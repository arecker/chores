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


def register(path, methods=[]):
    methods = sorted(['HEAD'] + methods)
    if not path.endswith('/') and not os.path.splitext(path)[1]:
        path += '/'

    def decorator(func):
        if path in ROUTES:
            logging.warning('oops, duplicate routes detected for %s!', path)

        route = Route(methods=methods, function=func)
        ROUTES[path] = route
        logging.info('registered route %s %s with %s()', path, route.methods,
                     route.function.__name__)

        return func

    return decorator


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args, **kwargs):
        pass

    def do(self):
        try:
            route = ROUTES[self.path]
            assert self.command in route.methods
        except KeyError:
            status = 404
            response = {'status': status, 'reason': 'page not found'}
        except AssertionError:
            status = 405
            response = {
                'status':
                status,
                'reason':
                '{} does not allow {} method, only {}'.format(
                    self.path, self.command, route.methods)
            }
        else:
            try:
                status, response = route.function()
            except Exception:
                logging.exception('%s on %s created unhandled exception',
                                  self.command, self.path)
                status = 500
                response = {
                    'status': status,
                    'reason': 'internal server error'
                }

        response = json.dumps(response, indent=2, sort_keys=True)
        response = response.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(response)
        return

    def do_HEAD(self):
        self.do()

    def do_GET(self):
        self.do()

    def do_POST(self):
        self.do()


@register('/info/', methods=['GET'])
def info():
    int('fish')
    return 200, {
        'datetime': datetime.datetime.now().isoformat(),
        'python_version': platform.python_version(),
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
