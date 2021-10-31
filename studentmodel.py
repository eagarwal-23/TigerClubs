from app import db

class Student(db.Model):
    __tablename__ = 'student_info'

    netid = db.Column(db.String(), primary_key = True)
    name = db.Column(db.String())
    res_college = db.Column(db.String())
    year = db.Column(db.Integer())
    major = db.Column(db.String())
    bio = db.Column(db.String())

def __init__(self, netid, name, res_college,
            year, major, bio):
    self._netid = netid
    self._name = name
    self._res_college = res_college
    self._year = year
    self._major = major
    self._bio = bio

def __repr__(self):
    return 'netid: ' + self.netid