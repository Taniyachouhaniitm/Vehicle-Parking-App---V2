from flask import Blueprint, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import ParkingLot, db, Reservation, ParkingSpot
import datetime
from flask import request
import sys
from datetime import datetime





user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard', methods=['GET'])
def user_dashboard():
    return jsonify({"msg": "Welcome to the user dashboard!"})


@user_bp.route('/available-lots', methods=['GET'])
@jwt_required()
def get_available_parking_lots():
    try:
        available_lots = ParkingLot.query.filter(ParkingLot.number_of_spots > 0).all()

        data = []
        for lot in available_lots:
            data.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'price': lot.price,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'number_of_spots': lot.number_of_spots,
                'reserved_spots': lot.reserved_spots
            })

        return jsonify(data), 200

    except Exception as e:
        return jsonify({'msg': 'Error fetching parking lots', 'error': str(e)}), 500
    

@user_bp.route('/available-lots/<int:lot_id>/book', methods=['POST'])
@jwt_required()
def book_spot(lot_id):
    user_id = get_jwt_identity()

    try:
        available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()

        if not available_spot:
            return jsonify({'msg': 'No available spots'}), 400

        reservation = Reservation(
            user_id=user_id,
            spot_id=available_spot.id,
            parking_timestamp=datetime.utcnow()
        )

        available_spot.status = 'O'

        db.session.add(reservation)  
        db.session.commit()

        return jsonify({
            'msg': 'Spot booked successfully',
            'reservation_id': reservation.id,
            'spot_id': available_spot.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': f'Server error: {str(e)}'}), 500


@user_bp.route('/reservations', methods=['GET'])
@jwt_required()
def user_reservations():
    try:
        user_id = get_jwt_identity()  # Get user ID from token

        reservations = Reservation.query.filter_by(user_id=user_id).all()
        data = []

        for r in reservations:
            data.append({
                'id': r.id,
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



@user_bp.route('/release-reservation/<int:reservation_id>', methods=['POST'])
@jwt_required()
def release_reservation(reservation_id):
    try:
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({'msg': 'Unauthorized'}), 401

        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return jsonify({'msg': 'Reservation not found'}), 404

        
        if reservation.leaving_timestamp:
            return jsonify({'msg': 'Already released'}), 400

        if not reservation.parking_timestamp:
            return jsonify({'msg': 'Missing parking timestamp'}), 500

        # Release reservation
        reservation.leaving_timestamp = datetime.now()

        # Calculate parking duration and cost
        duration_hours = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds() / 3600
        rate_per_hour = 50
        reservation.parking_cost = round(duration_hours * rate_per_hour, 2)

        # Mark parking spot as available
        spot = ParkingSpot.query.get(reservation.spot_id)
        if spot:
            spot.status = 'A'  

        db.session.commit()
        return jsonify({'msg': 'Reservation released successfully'}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'msg': f'Server error: {str(e)}'}), 500
