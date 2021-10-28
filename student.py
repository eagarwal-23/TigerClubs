#!/usr/bin/env python

#-----------------------------------------------------------------------
#   student.py
#   Authors: Eesha Agarwal and
#
class Student:
    def __init__(self, netid, name, res_college,
                year, major, clubs, interests, bio):
        self._netid = netid
        self._name = name
        self._res_college = res_college
        self._year = year
        self._major = major
        self._clubs = clubs
        self._interests = interests
        self._bio = bio

    def get_netid(self):
        return self._netid

    def get_name(self):
        return self._name

    def get_res_college(self):
        return self._res_college

    def get_year(self):
        return self._year

    def get_major(self):
        return self._major

    def get_clubs(self):
        return self._clubs

    def get_interests(self):
        return self._interests

    def get_bio(self):
        return self._bio
    
    def add_club(self, club):
        self._clubs.append(club.get_clubid())

    def add_interest(self, interest):
        self._clubs.append(interest.get_tagid())

    def set_bio(self, bio):
        self._bio = bio