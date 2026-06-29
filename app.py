from flask import Flask
from config import Config
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

app=create_app()
@app.route('/')
def home():
    return "Trekking Management Application Running Successfully!"
if __name__== "__main__":
    app.run(debug=True)