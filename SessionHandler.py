import Cookie
import base64
import time
import random
import pickle
import os

def generate_session_id(hostname):
    """Generate a session ID comprised of the user's hostname, the current time,
    and a random number

    :param hostname: Host requesting the session ID
    
    Returns a string."""
    pass

def fetch_session_by_id(id):
    """Fetch the requested session ID

    :param id: Session ID being requested by the client

    Returns a dictionary."""
    pass

def write_session(id, object):
    """Writes a session file to disk.

    :param id: Session ID being written to disk
    :param object: Python object to be pickled (serialized) and written to disk

    Returns nothing."""
    pass

class Session(object):

    def __init__(self, name = None):
        self._id = base64.b64encode('%s%s' % (time.localtime(), random.randint(10000000000, 100000000000)))[:32]

        if not name:
            self._name = 'SESSIONID'
        else:
            # TODO: Should validate the name against invalid characters
            self._name = name

        self._cookie = Cookie.SimpleCookie()
        self._cookie[self._name] = self._id

    @property
    def cookie(self):
        """Returns the session cookie"""
        return self._cookie

    @cookie.setter
    def cookie(self, value):
        """Sets the cookie"""
        self._cookie = value

    @property
    def id(self):
        """Returns the ID hash for the session"""
        return self._id

    def __repr__(self):
        if self._id:
            return self._id
        else:
            return repr(object)

    def __cmp__(self, session):
        return self._id == session.id
