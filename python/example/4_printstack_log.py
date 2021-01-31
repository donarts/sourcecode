import logging
import traceback 
import sys

logger = logging.getLogger('log')

A = [] 

try: 
    value = A[-1] 
      
except: 
    # printing stack trace 
    type, value, tb=sys.exc_info()
    ex_traceback=traceback.format_exception(type, value, tb) 

    print("1. print")
    for line in ex_traceback:
        print(line)

    print("2. log print")
    tb_lines = [line.rstrip('\n') for line in ex_traceback]
    logger.log(logging.ERROR,tb_lines)

print("end of program") 