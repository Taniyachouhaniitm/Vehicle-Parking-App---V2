from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import User, ParkingSpot, db, ParkingLot, Reservation
from flask_jwt_extended import get_jwt_identity


admin_bp = Blueprint('admin', __name__)

# Admin Dashboard
@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return jsonify({"msg": "Welcome to the admin dashboard!"})


# All Users
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user_id = get_jwt_identity()
    # Optionally verify admin user with ID

    users = User.query.all()
    user_list = [{
        "id": u.id,
        "username": u.username,
        "fname": u.fname,
        "lname": u.lname,
        "email": u.email,
        "role": u.role.name
    } for u in users]

    return jsonify(user_list), 200


# Parking Lots
@admin_bp.route('/parking_lots', methods=['POST'])
def create_parking_lot():
    data = request.get_json()
    
    # Create a new parking lot
    new_ParkingLot = ParkingLot(
        prime_location_name=data['name'],
        price=data['price'],
        address=data['address'],
        pin_code=data['pin_code'],
        number_of_spots=data['number_of_spots']
    )
    db.session.add(new_ParkingLot)
    db.session.commit()

    # Auto-generate parking spots
    for i in range(1, new_ParkingLot.number_of_spots + 1):
        spot = ParkingSpot(
            lot_id=new_ParkingLot.id,
            spot_number=f"Spot {i}",
            status='A'
        )
        db.session.add(spot)

    db.session.commit()

    return jsonify({"msg": "Parking lot created successfully!", 'lot_id': new_ParkingLot.id,
                     "created_at": new_ParkingLot.created_at.isoformat()}), 201


# Parking Spots
@admin_bp.route('/parking_spots', methods=['GET'])
@jwt_required()
def get_all_parking_spots():
    try:
        spots = ParkingSpot.query.all()
        data = [{
            'id': spot.id,
            'lot_id': spot.lot_id,
            'status': spot.status,
            'spot_number': spot.spot_number
        } for spot in spots]
        return jsonify(data), 200
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Error fetching parking spots'}), 500


# Get all parking spots for a lot
@admin_bp.route('/parking_spots/<int:lot_id>', methods=['GET'])
def get_parking_spots(lot_id):
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    spots_data = [
        {
            'id': spot.id,
            'lot_id': spot.lot_id,
            'spot_number': spot.spot_number,
            'status': spot.status
        }
        for spot in spots
    ]
    return jsonify(spots_data), 200

# Delete a parking spot
@admin_bp.route('/parking_spots/<int:spot_id>', methods=['DELETE'])
def delete_parking_spot(spot_id):
    spot = ParkingSpot.query.get(spot_id)

    if not spot:
        return jsonify({'message': 'Parking spot not found'}), 404

    db.session.delete(spot)
    db.session.commit()

    return jsonify({'message': 'Parking spot deleted successfully'}), 200


@admin_bp.route('/reservations', methods=['GET'])
@jwt_required()  
def view_reservations():
    try:
        reservations = Reservation.query.all()
        data = []

        for r in reservations:
            data.append({
                'id': r.id,
                'user_id': r.user_id,
                'spot_id': r.spot_id,
                'parking_timestamp': r.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.parking_timestamp else None,
                'leaving_timestamp': r.leaving_timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.leaving_timestamp else None,
                'parking_cost': r.parking_cost
            })

        return jsonify({'reservations': data}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'msg': f'Server error: {str(e)}'}), 500
