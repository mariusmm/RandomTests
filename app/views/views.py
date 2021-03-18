from pyramid.view import (
    view_config,
    view_defaults
    )

class Views:
    def __init__(self, request):
        self.request = request

    # landing view, avaliable at http://localhost:10000S
    @view_config(route_name='home', renderer='app:templates/home.jinja2')
    def home(self):
        return {'title': 'Tracker v0.1'}
