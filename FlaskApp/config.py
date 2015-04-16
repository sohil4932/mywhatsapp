# Configuratoin for this app
# All the global variable.
import os

class config():

	# Database URL
	SQLDATABASE_URI = 'mysql://root:hetvi_1234@localhost/mywhatsappdb'

	APP_ROOT = os.path.dirname(os.path.abspath(__file__))
	UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static')

	# message type for text message
	MESSAGE = 1

	# message type for image message
	IMAGE = 2