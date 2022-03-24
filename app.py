from flask import Flask
from application.db import db
from flask_restx import Api


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['JSON_AS_ASCII'] = False

    db.init_app(app)

    with app.app_context():

        api = Api(app)
        app.config['api'] = api
        from application import routes

        return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
