import cgi
import os
import mimetypes

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse

import fileParser

class RequestHandler(BaseHTTPRequestHandler):
    RENDERABLE_FILETYPES = ['htm', 'html', 'php']
    BINARY_FILETYPES = ['jpg', 'jpeg', 'gif', 'png']

    def __init__(self, app, *args, **kwargs):
        self.app = app
        self.setup_mime_types()
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
        
    def do_GET(self):
        try:
            requestType = self.headers.getheader('X-Requested-With')

            # AJAX requests have a content-type of x-www-form-urlencoded
            if requestType == 'XMLHttpRequest':
                url = urlparse(self.path)
                params = dict([part.split('=') for part in url[4].split('&')])

                requestPath = url[2].replace('/', '_').replace('.', '_')

                try:
                    get_request = getattr(self.app, 'GET%s' % requestPath)
                except AttributeError, e:
                    self.send_error(404, 'Error: %s' % e)
                else:
                    get_request(params)

            elif self.path:
                file = (self.path == '/') and 'index.php' or self.path[1:]
                
                self.send_file_response(file)()
        
        except IOError:
            self.send_error(404, 'File not found: %s' % self.path)
    
    # TODO: Implement POST
    def do_POST(self):
        pass

    def send_file_response(self, filename):
        extension = filename.split('.')[1]

        def render_page():
            self.send_headers()
            self.wfile.write(fileParser.get_file_contents(filename))

        def send_static_file():
            # Remove query string parameters
            parsedFilename = urlparse(filename)[2]

            mode = 'r'

            if extension in self.BINARY_FILETYPES:
                mode = 'rb'

            self.send_headers(value = mimetypes.guess_type(parsedFilename)[0])
            self.wfile.write(open(parsedFilename.replace('/', os.sep), mode).read())

        return (extension in self.RENDERABLE_FILETYPES) and render_page or send_static_file

    def send_headers(self, response = 200, key = 'Content-type', value = 'text/html'):
        self.send_response(response)
        self.send_header('Transfer-Encoding', 'chunked')
        self.send_header(key, value)
        self.end_headers()

    def setup_mime_types(self):
        mimetypes.add_type('text/css', '.css')
        mimetypes.add_type('application/x-javascript', '.js')
        mimetypes.add_type('image/png', '.png')

class App(object):
    def __init__(self, name, port):
        self.name = name
        self.port = port

    def Handler(self, *args, **kwargs):
        return RequestHandler(self, *args, **kwargs)

    def start(self):
        try:
            server = HTTPServer(('', self.port), self.Handler)
            server.serve_forever()
        except KeyboardInterrupt:
            server.socket.close()
