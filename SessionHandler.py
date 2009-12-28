import Cookie
import base64
import time
import random
import pickle
import os
from BaseHTTPServer import BaseHTTPRequestHandler

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

class Session(BaseHTTPRequestHandler, dict):
    def __init__(self, name = None, *args, **kwargs):
        self.data = {}

        if not name:
            self.name = 'SESSIONID'
        else:
            # TODO: Should validate the name against invalid characters
            self.name = name

        self.cookie = Cookie.SimpleCookie()
        self.cookie[self.name] = random.randint(10000000000, 100000000000)
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def send_cookie_headers(self):
        """Sends basic cookie headers to the client"""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def write_cookie_to_client(self):
        self.send_cookie_headers()
        self.wfile.write(str(self.cookie[self.name]))

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]
