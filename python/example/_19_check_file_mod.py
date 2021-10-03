import time
import os

class check_file_mod(object):
	def __init__(self,want_to_checkfile):
		self.filename = want_to_checkfile
		self._cached_stamp = os.stat(self.filename).st_mtime

	def is_change(self):
		stamp = os.stat(self.filename).st_mtime
		if stamp != self._cached_stamp:
			self._cached_stamp = stamp
			return True
		return False


if __name__ == '__main__':
	wa = check_file_mod("_19_check_file_mod.py")
	while True:
		if wa.is_change():
			print("change")
		time.sleep(1)
