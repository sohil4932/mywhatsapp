import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from werkzeug import secure_filename

# Import datbase models from db.py
from models import db, app, data

from config import config

import uuid

from flask import request

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Route request to 404 page during errors.
@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return "Hello World"

# Route that will process the text messages
@app.route('/message/<int:phone_number>/<text_message>', methods=['POST'])
def message(phone_number, text_message):
    # add data into table
    text_data = data(phone_number = str(phone_number), message_type = config.MESSAGE, data = str(text_message), status = 0)
    db.session.add(text_data)
    db.session.commit()
    # Get the data
    return "Succefully added " + text_message + " for " + str(phone_number)

# Route that will process the file upload
@app.route('/image/<int:phone_number>', methods=['POST'])
def upload(phone_number):
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = str(uuid.uuid4()) + ".jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(filepath)
        # add data into database
        image_data = data(phone_number = str(phone_number), message_type = config.IMAGE, data = str(filepath), status = 0)
        db.session.add(image_data)
        db.session.commit()
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return "Successful Upload for " + str(phone_number) 


if __name__ == '__main__':
    app.run()
