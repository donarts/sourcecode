import traceback 
import sys
A = [] 

try: 
    value = A[-1] 
      
except: 
    # printing stack trace 
    print("1. print_exc")
    traceback.print_exc() 
    print("2. print_exception")
    type, value, tb=sys.exc_info()
    traceback.print_exception(type, value, tb) 
  
print("end of program") 