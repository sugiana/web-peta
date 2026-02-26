from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
import zope.sqlalchemy
import configparser
import os
from models import Base


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager):
    dbsession = session_factory()
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager)
    return dbsession


def main():
    config_file = 'live.ini'
    config = configparser.ConfigParser()
    config.read(config_file)
    settings = dict(config['main'])

    # Absolute path for templates
    settings['pyramid.reload_templates'] = True

    engine = get_engine(settings)
    session_factory = get_session_factory(engine)

    with Configurator(settings=settings) as config:
        config.include('pyramid_chameleon')
        config.include('pyramid_tm')

        config.add_request_method(
            lambda r: get_tm_session(session_factory, r.tm),
            'dbsession',
            reify=True
        )

        config.add_static_view('static', 'static', cache_max_age=3600)
        config.add_route('home', '/')
        config.add_route('geojson', '/geojson')
        import views
        config.scan(views)

        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 6543, app)
    print("Serving at http://0.0.0.0:6543")
    server.serve_forever()


if __name__ == '__main__':
    main()
