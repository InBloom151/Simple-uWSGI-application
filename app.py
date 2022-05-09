from server import Application

def index_controller(env):
    return {
        'text': 'Hello, world',
        'extra_headers': {'Content-Type': 'text/plain'}
    }

def about_controller(env):
    return {
        'json': {'about': 'About'},
    }

application = Application()
application.add_controller('/', index_controller)
application.add_controller('/about/', about_controller)
