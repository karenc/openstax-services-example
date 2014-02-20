import cgi
import ConfigParser
import json
import time
import sys
import urlparse
from wsgiref.simple_server import make_server

import sanction

def redirect(environ, start_response, url):
    print 'Redirect to {}'.format(url)
    status = '302 Found'
    headers = [('Location', url)]
    start_response(status, headers)
    return []

class SimpleApp(object):

    def __init__(self, services_url, application_id, application_secret, app_url, port):
        self.resource_url = services_url
        self.authorize_url = urlparse.urljoin(self.resource_url, '/oauth/authorize')
        self.token_url = urlparse.urljoin(self.resource_url, '/oauth/token')
        self.application_id = application_id
        self.application_secret = application_secret
        self.redirect_uri = urlparse.urljoin(app_url, '/callback')
        self.port = port

        self.sanction_client = sanction.Client(auth_endpoint=self.authorize_url,
                                               token_endpoint=self.token_url,
                                               resource_endpoint=self.resource_url,
                                               client_id=self.application_id,
                                               client_secret=self.application_secret)

    def login(self, environ, start_response):
        return redirect(environ, start_response,
                        self.sanction_client.auth_uri(redirect_uri=self.redirect_uri))

    def callback(self, environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        output = []
        params = cgi.parse_qs(environ['QUERY_STRING'])
        code = params['code'][0]

        def parser(data):
            data = json.loads(data)
            if data.get('expires_in', '') is None:
                data.pop('expires_in')
            return data

        self.sanction_client.request_token(parser=parser,
                                           code=code,
                                           redirect_uri=self.redirect_uri)

        output.append('You are now logged in:\n\n')

        me = self.sanction_client.request('/api/v1/me.json')
        output += ['{}: {}\n'.format(k, v) for k, v in me.iteritems()]

        start_response(status, headers)
        return output

    def simple_app(self, environ, start_response):
        path_handlers = {
                '/login': self.login,
                '/callback': self.callback,
                }
        for path, handler in path_handlers.iteritems():
            if environ['PATH_INFO'].startswith(path):
                return handler(environ, start_response)

        status = '200 OK'
        headers = [('Content-type', 'text/html')]

        start_response(status, headers)

        return ['<html><body><a href="/login">Login</a></body></html>']

    def run(self):
        httpd = make_server('', 5000, self.simple_app)
        print 'Serving on port 5000...'
        httpd.serve_forever()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: {} config_file\n'.format(sys.argv[0]))
        sys.exit(1)

    config = ConfigParser.ConfigParser()
    config.read(sys.argv[1])
    services_url = config.get('example', 'services_url')
    application_id = config.get('example', 'application_id')
    application_secret = config.get('example', 'application_secret')
    app_url = config.get('example', 'app_url')
    port = config.getint('example', 'port')

    SimpleApp(services_url, application_id, application_secret, app_url,
              port).run()
