import base64
import time
import random
import pickle

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

class Session(dict):
    def __init__(self, id = None, hostname = None):
        if not id:
            self.id = generate_session_id(hostname)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]
