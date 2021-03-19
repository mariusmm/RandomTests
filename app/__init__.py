from pyramid.config import Configurator
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPSeeOther,
)
import os

def main(global_config, **settings):

    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('static_deform', 'deform:static')

    config.include('pyramid_jinja2')
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()

