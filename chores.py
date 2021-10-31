import collections
import datetime
import http.server
import json
import logging
import os
import platform
import sys

logging.basicConfig(stream=sys.stderr,
                    format='chores: %(message)s',
                    level=logging.INFO)

Route = collections.namedtuple('Route', 'methods function')
ROUTES = {}


def ensure_trailing_slash(path):
    if not path.endswith('/') and not os.path.splitext(path)[1]:
        return path + '/'
    else:
        return path


def register(path, methods=[]):
    methods = set(sorted(['HEAD', 'GET'] + methods))
    path = ensure_trailing_slash(path)

    def decorator(func):
        if path in ROUTES:
            logging.warning('oops, duplicate routes detected for %s!', path)

        route = Route(methods=methods, function=func)
        ROUTES[path] = route
        logging.info('registered route %s %s with %s()', path, route.methods,
                     route.function.__name__)

        return func

    return decorator


class HttpError(Exception):
    def __init__(self, status=0, reason=''):
        self.__dict__.update({'status': status, 'reason': reason})


Request = collections.namedtuple('Request', ['method', 'data'])
Response = collections.namedtuple('Response', ['status', 'data'])


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args, **kwargs):
        """Just overriding here to supress logging."""

    def calculate_route(self):
        path = ensure_trailing_slash(self.path)

        try:
            return ROUTES[path]
        except KeyError:
            message = f'no known route for {path}'
            raise HttpError(status=404, reason=message)

    def validate_method(self, route):
        try:
            assert self.command in route.methods
            return self.command
        except AssertionError:
            message = f'the {ensure_trailing_slash(self.path)} route'
            message += f'does not accept {self.command}'
            message += f', only {route.methods}'
            raise HttpError(status=405, reason=message)

    def extract_request_data(self):
        try:
            headers = dict([(k.upper(), v.upper())
                            for k, v in self.headers.items()])
            length = int(headers['CONTENT-LENGTH'])
        except KeyError:  # TODO: https://bugs.python.org/issue222756
            message = 'please supply valid "content-length" header'
            raise HttpError(status=400, reason=message)

        data = self.rfile.read(length)
        data = data.decode('utf-8')

        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            message = f'please supply valid json body with length of {length}'
            raise HttpError(status=400, reason=message)

    def execute_route(self, route, data):
        try:
            request = Request(method=self.command, data=data)
            status, data = route.function(request)
            return Response(status=status, data=data)
        except Exception as e:
            message = f'the {ensure_trailing_slash(self.path)}'
            message += ' route encountered a problem'

            logging.exception(e)
            raise HttpError(status=500, reason=message)

    def do(self):
        try:
            route = self.calculate_route()

            if self.validate_method(route) in ['POST', 'PUT']:
                data = self.extract_request_data()
            else:
                data = None
            response = self.execute_route(route=route, data=data)
        except HttpError as e:
            data = {'status': e.status, 'reason': e.reason}
            response = Response(status=e.status, data=data)

        logging.info('%s %s - %d - %s', self.command,
                     ensure_trailing_slash(self.path), response.status,
                     response.data)

        # send headers
        self.send_response(response.status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

        # send body
        body = json.dumps(response.data).encode('utf-8')
        self.wfile.write(body)

        # all done
        return

    def do_HEAD(self):
        self.do()

    def do_GET(self):
        self.do()

    def do_POST(self):
        self.do()


@register('/info/', methods=['GET', 'POST'])
def info(request):
    return 200, {
        'request_method': request.method,
        'request_data': request.data,
        'server_timestamp': datetime.datetime.now().isoformat(),
        'server_python_version': platform.python_version(),
    }


def main():
    logging.info('starting chores webserver (python %s, %s)',
                 platform.python_version(), sys.executable)

    httpd = http.server.HTTPServer(server_address=('', 8000),
                                   RequestHandlerClass=Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info('stopping webserver')


if __name__ == '__main__':
    main()
