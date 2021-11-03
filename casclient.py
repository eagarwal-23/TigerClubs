#!/usr/bin/env python

#-----------------------------------------------------------------------
# casclient.py
# Authors: Alex Halderman, Scott Karlin, Brian Kernighan, Bob Dondero
#-----------------------------------------------------------------------

from urllib.request import urlopen
from urllib.parse import quote
from re import sub
from flask import request, session, redirect, abort

#-----------------------------------------------------------------------

# Return url after stripping out the "ticket" parameter that was
# added by the CAS server.

def strip_ticket(url):
    if url is None:
        return "something is badly wrong"
    url = sub(r'ticket=[^&]*&?', '', url)
    url = sub(r'\?&?$|&$', '', url)
    return url

#-----------------------------------------------------------------------

class CasClient:

    #-------------------------------------------------------------------

    # Initialize a new CASClient object so it uses the given CAS
    # server, or fed.princeton.edu if no server is given.

    def __init__(self, url='https://fed.princeton.edu/cas/'):
        self.cas_url = url

    #-------------------------------------------------------------------

    # Validate a login ticket by contacting the CAS server. If
    # valid, return the user's username; otherwise, return None.

    def validate(self, ticket):
        val_url = (self.cas_url + "validate"
            + '?service=' + quote(strip_ticket(request.url))
            + '&ticket=' + quote(ticket))
        lines = []
        with urlopen(val_url) as flo:
            lines = flo.readlines()   # Should return 2 lines.
        if len(lines) != 2:
            return None
        first_line = lines[0].decode('utf-8')
        second_line = lines[1].decode('utf-8')
                                                                                                   1,1           Top
