from http.client import responses
import json


class Application:

    def __init__(self):
        self.controllers_map = {}

    def add_controller(self, path, controller_callable):
        self.controllers_map[path] = controller_callable

    def __call__(self, env, start_response):
        path = env['PATH_INFO']

        self.controllers_map = {
            '/': index_controller,
            '/about/': about_controller
        }

        controller = self.controllers_map.get(path, self.not_found_controller)

        response = controller()

        response_headers = {'Content-Type': 'text/html'}
        if 'text' in response:
            response_body = response['text']
        elif 'json' in response:
            response_body = json.dumps(response['json'])
            response_headers = {'Content-Type': 'text/json'}

        status_code = response.get('status_code', 200)
        extra_header = response.get('extra_header', {})
        response_headers.update(extra_header)

        start_response(f'{status_code} {responses[status_code]}', list(response_headers.items()))

        return [response_body.encode('utf-8')]

    @staticmethod
    def not_found_controller():
        return {
            'text': 'Not found',
            'status_code': 404
        }

def index_controller():
    return {
        'text': 'Hello, world',
        'extra_headers': {'Content-Type': 'text/plain'}
    }

def about_controller():
    return {
        'json': {'about': 'About'},
    }

application = Application()
application.add_controller('/', index_controller)
application.add_controller('/about/', about_controller)
