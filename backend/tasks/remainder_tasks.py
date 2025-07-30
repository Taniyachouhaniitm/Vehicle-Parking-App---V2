from datetime import datetime, timedelta
from celery import shared_task
from app import create_app  
from models import User, Reservation, ParkingLot
from utils.mail import send_email

flask_app = create_app()

@shared_task
def send_daily_reminder():
    with flask_app.app_context():
        cutoff_time = datetime.now() - timedelta(days=3)
        inactive_users = User.query.outerjoin(Reservation).filter(
            (Reservation.parking_timestamp == None) | 
            (Reservation.parking_timestamp < cutoff_time)
        ).all()

        parking_lots = ParkingLot.query.all()
        lot_names = ", ".join([lot.prime_location_name for lot in parking_lots])

        for user in inactive_users:
            subject = "Daily Parking Reminder"
            body = f"Hi {user.username},\n\nDon't forget to book your parking space today!\n\nAvailable lots: {lot_names}"
            send_email(user.email, subject, body)