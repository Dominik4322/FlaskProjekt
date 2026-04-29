from flask import Flask
from extensions import db
from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "super-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from routes import main
    app.register_blueprint(main)

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        from models import Game
        db.create_all()

    app.run(debug=True)