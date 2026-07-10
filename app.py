from flask import Flask
from config import Config
from models import db
from routes.auth import auth_bp
from routes.user import user_bp
from routes.staff import staff_bp
from routes.admin import admin_bp
from routes.api import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(api_bp)
    return app

app=create_app()
if __name__== "__main__":
    app.run(debug=True)