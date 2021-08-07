from flask import Flask

from webapp.ext import configuration


def minimal_app():
    app = Flask(__name__, static_folder="blueprints/frontend/static")
    configuration.init_app(app)
    return app


def create_app():
    app = minimal_app()
    configuration.load_extensions(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
