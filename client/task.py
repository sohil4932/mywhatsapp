from sqlalchemy import Column, Date, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Data

import sys

from mywhatsapp import send_message
from config import config

engine = create_engine(config.SQLDATABASE_URI)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()


def do_task():

	count = session.query(Data).filter(Data.status==0).count()

	if count > 0:

		# Get data from table
		res = session.query(Data).filter(Data.status==0).first()

		try:
			destination = str(res.phone_number)
			message = str(res.data)
			message_type = str(res.message_type)
			print "sending message to" + destination + "with message_type" + message_type
			send_message(destination, message, message_type)
		except KeyboardInterrupt:
			print('closing')
			res.status = 1
			session.commit()
			if message_type == config.IMAGE:
				## delete only if file exists ##
				if os.path.exists(message):
					try:
						os.remove(message)
					except IOError:
						print("Sorry, I can not remove %s file." % message)
						pass
				else:
					print("Sorry, I can not remove %s file." % message)
			sys.exit(0)

	else:
		# exit thread
		sys.exit(0)


        


	
