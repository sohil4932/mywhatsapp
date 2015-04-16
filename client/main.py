import sys

from threading import Thread
import time
from task import do_task

var = 1

while var == 1:

	thr = Thread(target = do_task, args = [])
	thr.start()

	try:
		print("sleeping for a minute")
		time.sleep(60)
	except KeyboardInterrupt:
		print("closing")
		sys.exit(0)




