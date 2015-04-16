# Models for this application

# Import sqlalchemy : http://pythonhosted.org/Flask-SQLAlchemy/
from flask.ext.sqlalchemy import SQLAlchemy

# Import Flask
from flask import Flask

# Import Configuration for this app
from config import config

# Create main application object of Flask App
app = Flask(__name__)

# Configure app with our Database.
# TODO : Change this database URL with our main database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLDATABASE_URI

app.config['SERVER_NAME'] = '127.0.0.1'

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

# Create database object.
db = SQLAlchemy(app)

# Model for Product Type
class data(db.Model):
	__tablename__ = 'db_data'
	id = db.Column(db.Integer, primary_key = True)
	phone_number = db.Column(db.Integer)
	message_type = db.Column(db.Integer)
	data = db.Column(db.String(255))
	status = db.Column(db.Integer)