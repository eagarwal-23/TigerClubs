#!/usr/bin/env python

#-----------------------------------------------------------------------
#   student.py
#   Authors: Eesha Agarwal and
#
class Student:
    def __init__(self, netid, name, email, res_college,
                year, major, prgm_study, clubs):
        self._netid = netid
        self._name = name
        self._email = email
        self._res_college = res_college
        self._year = year
        self._major = major
        self._prgm_study = prgm_study
        self._clubs = clubs

    def get_netid(self):
        return self._netid

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    def get_res_college(self):
        return self._res_college

    def get_year(self):
        return self._year

    def get_major(self):
        return self._major

    def get_prgm_study(self):
        return self._prgm_study

    def get_clubs(self):
        return self._clubs
    
    def add_club(self, clubs):
        for club in clubs:
            self.clubs.append(club.get_clubidd())