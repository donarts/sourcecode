import _17_logger_color
import _17_logger_color_test_2

logger = _17_logger_color.CustomLog().create('log',__name__)

if __name__ == "__main__":
	_17_logger_color_test_2.noncolor_test()

	logger.debug("debug test")
	logger.info("info test")
	logger.warning("warning test")
	logger.error("error test")
	logger.critical("critical test")
	
	logger = _17_logger_color.CustomLog().create('log',__name__,color=False)
	logger.debug("MAIN color false test")
	logger.info("info test")
	logger.warning("warning test")
	logger.error("error test")
	logger.critical("critical test")
	
	_17_logger_color_test_2.noncolor_test()