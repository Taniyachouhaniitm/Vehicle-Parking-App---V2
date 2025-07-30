from celery_app import celery
from models import db, Reservation, User, ParkingSpot, ParkingLot
from utils.mail import send_file_email
import csv
import io
from datetime import datetime


@celery.task(name='tasks.csv_tasks.export_reservations_to_csv')
def export_reservations_to_csv(user_email):
    reservations = db.session.query(
        Reservation.id,
        User.email,
        User.username,
        ParkingSpot.spot_number,
        ParkingLot.prime_location_name,
        Reservation.parking_timestamp,
        Reservation.leaving_timestamp,
        Reservation.parking_cost
    ).join(User).join(ParkingSpot).join(ParkingLot).all()

    if not reservations:
        return "No reservations found."

    csv_io = io.StringIO()
    writer = csv.writer(csv_io)
    writer.writerow([
        "Reservation ID", "Email", "Username", "Spot Number",
        "Lot Location", "Parked At", "Left At", "Cost"
    ])

    for res in reservations:
        writer.writerow([
            res.id,
            res.email,
            res.username,
            res.spot_number,
            res.prime_location_name,
            res.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            res.leaving_timestamp.strftime("%Y-%m-%d %H:%M:%S") if res.leaving_timestamp else "",
            res.parking_cost if res.parking_cost else 0.0
        ])

    csv_io.seek(0)
    subject = "CSV Export - Reservations Report"
    filename = f"reservations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    send_file_email(user_email, subject, csv_io.read(), filename)

    return f"CSV sent to {user_email}"
