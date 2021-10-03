import _17_logger_color

logger = _17_logger_color.CustomLog().create('log',__name__,color=False)

def noncolor_test():
	logger.debug("debug test 2")
	logger.info("info test 2")
	logger.warning("warning test 2")
	logger.error("error test 2")
	logger.critical("critical test 2")

