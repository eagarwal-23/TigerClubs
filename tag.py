#!/usr/bin/env python

#-----------------------------------------------------------------------
#   tag.py
#   Authors: Eesha Agarwal and
#
class Tag:
    def __init__(self, name, tagid):
        self._name = name
        self._tagid = tagid

    def get_name(self):
        return self._name

    def get_tagid(self):
        return self._tagid

    def __repr__(self):
        return ("tag: " + self.name)