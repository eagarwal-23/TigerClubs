#!/usr/bin/env python

#-----------------------------------------------------------------------
#   club.py
#   Authors: Eesha Agarwal and
#
class Club:
    def __init__(self, clubid, name, desc,
                officers, tags):
        self._clubid = clubid
        self._name = name
        self._desc = desc
        self._officers = officers
        self._tags = tags

    def get_clubid(self):
        return self._clubid

    def get_name(self):
        return self._name

    def get_desc(self):
        return self._desc

    def get_officers(self):
        return self._officers

    def get_tags(self):
        return self._tags

    def add_officers(self, officers):
        for officer in officers:
            self._officers.append(officer.get_netid())

    def add_tags(self, tags):
        for tag in tags:
            self._officers.append(tags.get_tagid())