from pyramid.config import Configurator
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPSeeOther,
)

def main(global_config, **settings):

    # threading._start_new_thread(gen.run())
    # calc_thread = threading.Thread(target=gen.run())
    # calc_thread.setDaemon(True)
    # calc_thread.start()
    

    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('static_deform', 'deform:static')

    config.include('pyramid_jinja2')
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()

