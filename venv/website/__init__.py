from flask import Flask, app


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ZIGZAGPY-SECRET-KEY'

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app
