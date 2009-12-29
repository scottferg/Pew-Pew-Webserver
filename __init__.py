import cgi
import os
import sys
import mimetypes
import StringIO
import re
import json
import Cookie

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse

import fileParser

class RequestHandler(BaseHTTPRequestHandler):
    RENDERABLE_FILETYPES = ['htm', 'html']
    BINARY_FILETYPES = ['jpg', 'jpeg', 'gif', 'png']

    def __init__(self, app, *args, **kwargs):
        """Constructor for a request handler.

        :param app: Application hosting the handler
        """
        self.app = app
        self.setup_mime_types()
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
        
    def do_GET(self):
        """Response for a GET request"""
        try:
            requestType = self.headers.getheader('X-Requested-With')

            # AJAX requests have a content-type of x-www-form-urlencoded
            if requestType == 'XMLHttpRequest':
                url = urlparse(self.path)

                # Set params to an empty dictionary if none are provided
                try:
                    params = dict([part.split('=') for part in url[4].split('&')])
                except ValueError:
                    params = {}

                # Add the client's hostname to the parameter list
                params['client'] = self.headers.getheader('Host')

                # Turn some/request/path into some_request_path
                requestPath = url[2].replace('/', '_').replace('.', '_')

                try:
                    get_request = getattr(self.app, 'GET%s' % requestPath)
                except AttributeError, e:
                    self.send_error(404, 'Error: %s' % e)
                else:
                    self.send_data_response(get_request(params))

            elif self.path:
                file = (self.path == '/') and 'index.html' or self.path[1:]
                
                self.send_file_response(file)()
        
        except IOError:
            self.send_error(404, 'File not found: %s' % self.path)
    
    # TODO: Implement POST
    def do_POST(self):
        """Response for a POST request"""
        pass

    def send_file_response(self, filename):
        """Provides the appropriate response based upon the type of
        file being requested

        :param filename: String representing the relative filename being requested

        Returns a function.
        """
        extension = filename.split('.')[1]
        
        def render_page():
            """Renders an HTML page"""
            self.send_headers()
            self.wfile.write(fileParser.get_file_contents(filename))

        def send_static_file():
            """Response which handles non-renderable binary filetypes"""
            # Remove query string parameters
            parsedFilename = urlparse(filename)[2]

            mode = 'r'

            if extension in self.BINARY_FILETYPES:
                mode = 'rb'

            self.send_headers(value = mimetypes.guess_type(parsedFilename)[0])
            self.wfile.write(open(parsedFilename.replace('/', os.sep), mode).read())

        return (extension in self.RENDERABLE_FILETYPES) and render_page or send_static_file

    def send_data_response(self, params):
        """Sends the response provided by the client application

        :param params: Dictionary of parameters to send
        """
        self.send_headers(value = 'text/plain')
        self.wfile.write(json.dumps(params))

    def send_headers(self, response = 200, key = 'Content-type', value = 'text/html'):
        """Sends basic headers to the client

        :param response: HTTP response code, defaults to 200
        :param key: Header key, defaults to 'Content-type'
        :param value: Header value, defaults to 'text/html'
        """
        self.send_response(response)
        self.send_header(key, value)

        if self.app.session:
            sessionID = 'pysessid=' + self.app.session.id
            self.send_header('Set-Cookie', sessionID)
    
        self.end_headers()

    def setup_mime_types(self):
        """Sets mimetypes for irregular files"""
        mimetypes.add_type('text/css', '.css')
        mimetypes.add_type('application/x-javascript', '.js')
        mimetypes.add_type('image/png', '.png')

class App(object):

    def __init__(self, name, port):
        """Constructor for an App

        :param name: Name of the application
        :param port: Port to run the application on
        """
        self._name = name
        self._port = port
        self._session = None

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    @property
    def address(self):
        """Returns the hostname of the running server"""
        return self._server.server_name

    def Handler(self, *args, **kwargs):
        """Returns the request handler for the app"""
        return RequestHandler(self, *args, **kwargs)

    def start(self):
        """Starts up the application on it's specified port"""
        try:
            self._server = HTTPServer(('', self._port), self.Handler)
            self._server.serve_forever()
        except KeyboardInterrupt:
            self._server.socket.close()
