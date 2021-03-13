import traceback 

print("string format")
print('We are the {} who say "{}!"'.format('knights', 'Ni'))
# 기본 사용 : 순차적
# We are the knights who say "Ni!"

print('{1} and {0}'.format('spam', 'eggs'))
# 기본 사용 : 순서를 바꿀 수 있음
# eggs and spam

print('This {food} is {adjective}.'.format(adjective='absolutely horrible',food='spam'))
# 기본 사용 : 변수 별로 처리 가능
# This spam is absolutely horrible.


print_string ="Hello{pwantdata}pwantdata{pwantdata}|{KK}|{float_data}|"
print_string = print_string.format(pwantdata=123,KK="123",float_data=1.2)
print(print_string)
# {pwantdata} 여러개가 있더라도 처리
# Hello123pwantdata123|123|1.2|

print_string ="Hello{pwantdata}pwantdata{pwantdata}|{KK}|{float_data}|"
data_dict = {"pwantdata":123,"KK":"123","float_data":1.2}
print_string = print_string.format(**data_dict)
print(print_string)
# dictionary로 표현할때 <**> 사용
# Hello123pwantdata123|123|1.2|


print_string ="pwantdata" 
print_string = print_string.format(pwantdata_1=123)
print(print_string)
# pwantdata_1 없더라도 No Error
# pwantdata

try:
	print_string ="{pwantdata}}" 
	print_string = print_string.format(pwantdata=123) # Error 
except:
	traceback.print_exc()
'''
괄호가 안맞으면 오류
Traceback (most recent call last):
  File "6_string_format.py", line 29, in <module>
    print_string = print_string.format(pwantdata=123) # Error
ValueError: Single '}' encountered in format string
'''

try:
	print_string ="{pwantdata}" 
	print_string = print_string.format(pwantdata_1=123) # Error
except:
	traceback.print_exc()
'''
괄호안의 데이터가 인자로 주어지지 않으면 오류
Traceback (most recent call last):
  File "6_string_format.py", line 35, in <module>
    print_string = print_string.format(pwantdata_1=123) # Error
KeyError: 'pwantdata'
'''