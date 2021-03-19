from pyramid.view import (
    view_config,
    view_defaults
    )

class Views:
    def __init__(self, request):
        self.request = request
        # self.apikey = 'AIzaSyBIwzALxUPNbatRBj3Xi1Uhp0fFzwWNBkE' #random key
        self.apikey = 'AIzaSyBrx8kb5saOxbKlKuMVFXDKirqLR0eezeE' #IEEC temp apikey
    # landing view, avaliable at http://localhost:10000S
    @view_config(route_name='home', renderer='app:templates/tracker.jinja2')
    def home(self):
        return {'title': 'Tracker v0.1', 'apikey': self.apikey}