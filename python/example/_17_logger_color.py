import datetime
import sys
import os
import time
import logging
import colorlog
from logging import FileHandler
from logging import handlers

class CustomLog:
	def __init__(self):
		pass
		
	def create(self,logfolder='', app_name=__name__, logprefix='log_', NEED_BACKUP_FILE = True, NEED_SCREEN_AND_FILE = True, level=logging.DEBUG, format='[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', maxBytes=10*1024*1024, backupCount = 10, encoding='utf-8', color=True):
		LOG_PREFIX = logprefix
		LOG_FOLDER_NAME = logfolder
		# 로그 파일 핸들러
		now = datetime.datetime.now().isoformat()[:10]
		logf = LOG_PREFIX + now + ".log"
		if LOG_FOLDER_NAME!='' and not os.path.exists(LOG_FOLDER_NAME):
			os.makedirs(LOG_FOLDER_NAME)
		logf = os.path.join(LOG_FOLDER_NAME, logf)
		logger = self.getLogger(logf, app_name, NEED_BACKUP_FILE, NEED_SCREEN_AND_FILE, level, format, maxBytes, backupCount, encoding, color)
		logger.logfilename_ = logf
		return logger

	def getLogger(self, filename, app_name, NEED_BACKUP_FILE, NEED_SCREEN_AND_FILE, level, format, maxBytes, backupCount, encoding, color):
		if color :
			self.logger = colorlog.getLogger(app_name)
		else:
			self.logger = logging.getLogger(app_name)
		
		self.logger.handlers.clear()
		self.logger.propagate = False
		# log level은 아래 순서에 따른다. setLevel 과 같거나 큰 출력만 나오게 된다.
		# logger.setLevel(logging.CRITICAL) 인 경우 logger.critical() 만 나온다
		#
		# logger.debug("debug")
		# logger.info("info")
		# logger.warning("warning")
		# logger.error("error")
		# logger.critical("critical")
		self.logger.setLevel(level)

		# 포맷을 결정한다. 좀더 자세한 정보는 다음 링크를 참조한다
		# https://docs.python.org/3/library/logging.html#logrecord-attributes
		if color :
			logFormatter = colorlog.ColoredFormatter('%(log_color)s'+format)
		else :
			logFormatter = logging.Formatter(format)
		
		if NEED_BACKUP_FILE == True:
			rotatingHandler = handlers.RotatingFileHandler(filename=filename, maxBytes=maxBytes, backupCount = backupCount, encoding=encoding)
			rotatingHandler.setFormatter(logFormatter)
			self.logger.addHandler(rotatingHandler)
		else:
			fileHandler = logging.FileHandler(filename)
			fileHandler.setFormatter(logFormatter)
			self.logger.addHandler(fileHandler)

		# StreamHandler 는 self.logger.critical("critical") 이런 형태의 로그가 화면으로도 나오고 file로도 저장이 되도록 한다
		if NEED_SCREEN_AND_FILE == True:
			streamHandler = logging.StreamHandler()
			streamHandler.setFormatter(logFormatter)
			self.logger.addHandler(streamHandler)
		return self.logger
	
if __name__ == "__main__":
	logger = CustomLog().create('log')
	print("test")
	logger.debug("debug test")
	logger.info("info test")
	logger.warning("warning test")
	logger.error("error test")
	logger.critical("critical test")
	'''
	# other file
	import _17_logger_color
	logger = _17_logger_color.CustomLog().create('log',__name__)

	if __name__ == "__main__":
		logger.debug("debug test")
		logger.info("info test")
		logger.warning("warning test")
		logger.error("error test")
		logger.critical("critical test")
	'''