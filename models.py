from app import db

# association tables
student_clubs = db.Table('student_clubs', 
                          db.Column('netid', db.String(), db.ForeignKey('student_info.netid')),
                          db.Column('clubid', db.Integer(), db.ForeignKey('club_info.clubid')))

student_tags = db.Table('student_tags', 
                        db.Column('netid', db.String(), db.ForeignKey('student_info.netid')),
                        db.Column('tagid', db.Integer(), db.ForeignKey('tag_info.tagid')))

club_tags = db.Table('club_tags', 
                        db.Column('clubid', db.Integer(), db.ForeignKey('club_info.clubid')),
                        db.Column('tagid', db.Integer(), db.ForeignKey('tag_info.tagid')))

# models
class Student(db.Model):
    __tablename__ = 'student_info'

    netid = db.Column(db.String(), primary_key = True)
    name = db.Column(db.String())
    res_college = db.Column(db.String())
    year = db.Column(db.Integer())
    major = db.Column(db.String())
    bio = db.Column(db.String())
    clubs = db.relationship("Club",
                               secondary=student_clubs)

    tags = db.relationship("Tag",
                               secondary=student_tags)

    def __init__(self, netid, name, res_college,
            year, major, bio):
        self._netid = netid
        self._name = name
        self._res_college = res_college
        self._year = year
        self._major = major
        self._bio = bio

    def __repr__(self):
        return self.netid

class Club(db.Model):
    __tablename__ = 'club_info'

    # auto-increment is automatic
    clubid = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    members = db.relationship("Student",
                               secondary=student_clubs)
    tags = db.relationship("Tag",
                               secondary=club_tags)

    def __init__(self, name, description):
        self._name = name
        self.description = description

    def __repr__(self):
        return self.name

class Tag(db.Model):
    __tablename__ = 'tag_info'

    # auto-increment is automatic
    tagid = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String())

    students = db.relationship("Student",
                               secondary=student_tags)

    clubs = db.relationship("Tag",
                               secondary=club_tags)

    def __init__(self, name, desc):
        self._name = name

    def __repr__(self):
        return self.name 