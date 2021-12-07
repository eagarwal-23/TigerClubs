from app import db
from models import Rating_Period

def get_rating_period():
    rating_period = Rating_Period.query.filter_by(id = 1).first()
    print("this is the rating period", rating_period)
    return rating_period

def set_rating_period(day, month, year):
    rating_period = Rating_Period.query.filter_by(id = 1).first()
    rating_period.day = day
    rating_period.month = month
    rating_period.year = year

    db.session.add(rating_period)
    db.session.commit()