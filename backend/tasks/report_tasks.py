from flask_mail import Message
from app import mail, app
from extensions import db
from celery_app import make_celery
from models import Reservation, User
from datetime import datetime

celery = make_celery(app)

@celery.task
def send_monthly_report():
    with app.app_context():
        first_day = datetime.utcnow().replace(day=1)
        reservations = Reservation.query.filter(Reservation.start_time >= first_day).all()

        user_data = {}
        for res in reservations:
            user_data.setdefault(res.user_id, []).append(res)

        for user_id, res_list in user_data.items():
            user = User.query.get(user_id)
            if user and user.email:
                body = f"Monthly Parking Summary for {user.name}\n"
                for res in res_list:
                    body += f"Reservation at Lot {res.lot_id} on {res.start_time}\n"
                msg = Message("Monthly Parking Report", recipients=[user.email], body=body)
                mail.send(msg)
