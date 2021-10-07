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
		self.rotatingHandler = None
		self.fileHandler = None
		self.streamHandler = None
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
			self.rotatingHandler = handlers.RotatingFileHandler(filename=filename, maxBytes=maxBytes, backupCount = backupCount, encoding=encoding)
			self.rotatingHandler.setFormatter(logFormatter)
			self.logger.addHandler(self.rotatingHandler)
		else:
			self.fileHandler = logging.FileHandler(filename)
			self.fileHandler.setFormatter(logFormatter)
			self.logger.addHandler(self.fileHandler)

		# StreamHandler 는 self.logger.critical("critical") 이런 형태의 로그가 화면으로도 나오고 file로도 저장이 되도록 한다
		if NEED_SCREEN_AND_FILE == True:
			self.streamHandler = logging.StreamHandler()
			self.streamHandler.setFormatter(logFormatter)
			self.logger.addHandler(self.streamHandler)
		return self.logger
	def setLevel(self,filelevel,streamlevel):
		if self.rotatingHandler :
			self.rotatingHandler.setLevel(filelevel)
		if self.fileHandler :
			self.fileHandler.setLevel(filelevel)
		if self.streamHandler :
			self.streamHandler.setLevel(streamlevel)
		
	
	
if __name__ == "__main__":
	LOG = CustomLog()
	logger = LOG.create('log')
	print("test")
	logger.debug("debug test")
	logger.info("info test")
	logger.warning("warning test")
	logger.error("error test")
	logger.critical("critical test")
	LOG.setLevel(filelevel=logging.INFO,streamlevel=logging.ERROR)
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
'''
test
[2021-10-07 20:38:50,724] DEBUG [_23_logger_multi_level.py.<module>:84] debug test
[2021-10-07 20:38:50,725] INFO [_23_logger_multi_level.py.<module>:85] info test
[2021-10-07 20:38:50,726] WARNING [_23_logger_multi_level.py.<module>:86] warning test
[2021-10-07 20:38:50,728] ERROR [_23_logger_multi_level.py.<module>:87] error test
[2021-10-07 20:38:50,729] CRITICAL [_23_logger_multi_level.py.<module>:88] critical test
[2021-10-07 20:38:50,730] ERROR [_23_logger_multi_level.py.<module>:93] error test
[2021-10-07 20:38:50,731] CRITICAL [_23_logger_multi_level.py.<module>:94] critical test
~~~~~~~~~~~~~~~ LOG FILE ~~~~~~~~~~~~~~~~~~~~~
[37m[2021-10-07 20:38:50,724] DEBUG [_23_logger_multi_level.py.<module>:84] debug test[0m
[32m[2021-10-07 20:38:50,725] INFO [_23_logger_multi_level.py.<module>:85] info test[0m
[33m[2021-10-07 20:38:50,726] WARNING [_23_logger_multi_level.py.<module>:86] warning test[0m
[31m[2021-10-07 20:38:50,728] ERROR [_23_logger_multi_level.py.<module>:87] error test[0m
[1;31m[2021-10-07 20:38:50,729] CRITICAL [_23_logger_multi_level.py.<module>:88] critical test[0m
[32m[2021-10-07 20:38:50,730] INFO [_23_logger_multi_level.py.<module>:91] info test[0m
[33m[2021-10-07 20:38:50,730] WARNING [_23_logger_multi_level.py.<module>:92] warning test[0m
[31m[2021-10-07 20:38:50,730] ERROR [_23_logger_multi_level.py.<module>:93] error test[0m
[1;31m[2021-10-07 20:38:50,731] CRITICAL [_23_logger_multi_level.py.<module>:94] critical test[0m

'''