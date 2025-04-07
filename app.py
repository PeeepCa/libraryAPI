from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)

# Import routes after db initialization
from routes import *

if __name__ == '__main__':
    with app.app_context(): db.create_all()  # Create database tables
    app.run(debug=True)
