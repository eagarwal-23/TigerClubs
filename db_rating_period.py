from app import db
from models import Rating_Period

def get_rating_period():
    start_rating_period = Rating_Period.query.filter_by(id = 1).first()
    end_rating_period = Rating_Period.query.filter_by(id = 2).first()
    return start_rating_period, end_rating_period

def set_start_rating_period(day, month, year):
    rating_period = Rating_Period.query.filter_by(id = 1).first()
    rating_period.day = day
    rating_period.month = month
    rating_period.year = year

    db.session.add(rating_period)
    db.session.commit()

def set_end_rating_period(day, month, year):
    rating_period = Rating_Period.query.filter_by(id = 2).first()
    rating_period.day = day
    rating_period.month = month
    rating_period.year = year

    db.session.add(rating_period)
    db.session.commit()