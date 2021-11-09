from app import db

# association tables
student_clubs = db.Table('student_clubs', 
                          db.Column('netid', db.String(), db.ForeignKey('student_info.netid')),
                          db.Column('clubid', db.Integer(), db.ForeignKey('club_info.clubid')))

student_tags = db.Table('student_tags', 
                        db.Column('netid', db.String(), db.ForeignKey('student_info.netid')),
                        db.Column('tagid', db.Integer(), db.ForeignKey('tag_info.tagid')))

student_reviews = db.Table('student_reviews', 
                        db.Column('reviewid', db.Integer(), db.ForeignKey('review_info.reviewid')),
                        db.Column('netid', db.String(), db.ForeignKey('student_info.netid')))

club_tags = db.Table('club_tags', 
                        db.Column('clubid', db.Integer(), db.ForeignKey('club_info.clubid')),
                        db.Column('tagid', db.Integer(), db.ForeignKey('tag_info.tagid')))

club_reviews = db.Table('club_reviews', 
                        db.Column('reviewid', db.Integer(), db.ForeignKey('review_info.reviewid')),
                        db.Column('clubid', db.Integer(), db.ForeignKey('club_info.clubid')))

# models
class Student(db.Model):
    __tablename__ = 'student_info'

    netid = db.Column(db.String(), primary_key = True)
    name = db.Column(db.String())
    res_college = db.Column(db.String())
    year = db.Column(db.String())
    major = db.Column(db.String())
    bio = db.Column(db.String())
    admin = db.Column(db.Boolean())
    clubs = db.relationship("Club",
                                secondary=student_clubs)

    tags = db.relationship("Tag",
                                secondary=student_tags)

    reviews = db.relationship("Review",
                                secondary=student_reviews)

    def __init__(self, netid, name, res_college,
            year, major, bio, admin=False):
        self.netid = netid
        self.name = name
        self.res_college = res_college
        self.year = year
        self.major = major
        self.bio = bio
        self.admin= admin

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
    reviews = db.relationship("Review",
                               secondary=club_reviews)

    def __init__(self, name, description = None):
        self.name = name
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

    clubs = db.relationship("Club",
                               secondary=club_tags)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Review(db.Model):
    __tablename__ = 'review_info'

    # auto-increment is automatic
    print('oh god')
    reviewid = db.Column(db.Integer(), primary_key = True)
    print('hm')
    diversity = db.Column(db.Integer())
    inclusivity = db.Column(db.Integer())
    time_commitment = db.Column(db.Integer())
    experience_requirement = db.Column(db.Integer())
    workload = db.Column(db.Integer())
    student = db.relationship("Student",
                               secondary=student_reviews,
                               post_update=True)
    club = db.relationship("Club",
                               secondary=club_reviews,
                               post_update=True)

    def __init__(self, diversity, inclusivity, time_commitment, experience_requirement, workload):
        self.diversity = diversity
        self.inclusivity = inclusivity
        self.time_commitment = time_commitment
        self.experience_requirement = experience_requirement
        self.workload = workload

    def __repr__(self):
        str_review = "Club: " + str(self.club[0]) + '\n'
        str_review += 'Diversity: ' + str(self.diversity) + '\n'
        str_review += 'Inclusivity: ' + str(self.inclusivity) + '\n'
        str_review += 'Time Commitment: ' + str(self.time_commitment) + '\n'
        str_review += 'Experience required: ' + str(self.experience_requirement) + '\n'
        str_review += 'Workload: ' + str(self.workload) + '\n'

        return str_review
