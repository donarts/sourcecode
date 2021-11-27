import datetime

#현재 시각을 출력합니다.
nowtime = datetime.datetime.now()
print(type(nowtime))
print(str(nowtime))
print(nowtime)
'''
<class 'datetime.datetime'>
2021-10-31 21:56:33.981906
2021-10-31 21:56:33.981906
'''


# 포맷된 출력을 원하는 경우 strftime()
# https://docs.python.org/ko/3/library/datetime.html?highlight=now#strftime-and-strptime-format-codes
print(nowtime.strftime("%Y-%m-%d %H:%M:%S.%f"))
print(nowtime.strftime("%Y-%B-%d %A %H:%M:%S.%f"))
strtime = str(nowtime.strftime("%Y-%B-%d %A %H:%M:%S.%f"))
'''
2021-10-31 21:56:33.981906
2021-October-31 Sunday 21:56:33.981906
'''


# 시간 문자열을 읽으려면 strptime()
# https://docs.python.org/ko/3/library/datetime.html?highlight=now#strftime-and-strptime-format-codes
getdatetime1 = datetime.datetime.strptime("2021-01-02 20:21:11.981906","%Y-%m-%d %H:%M:%S.%f")
print(getdatetime1)
'''
2021-01-02 20:21:11.981906
'''

# 일부 값이 없다면 - 기본값이 들어갑니다. 초기값은 0년이 아니라 1900년이 됩니다.
getdatetime2 = datetime.datetime.strptime("01-02 20:21:11.981906","%m-%d %H:%M:%S.%f")
print(getdatetime2)
'''
1900-01-02 20:21:11.981906
'''

# 시간차 계산이 가능합니다.
tdelta = getdatetime1-getdatetime2
print(tdelta)
'''
44195 days, 0:00:00
'''

# 초로 표현해봅시다.
print(tdelta.total_seconds())
'''
3818448000.0
'''

# 년을 계산하려면 365로 나누어 줍니다.
# 1년이 정확히 365일이 아니기 때문에 나누어 떨어지지는 않습니다.
print(tdelta.days / 365)
'''
121.08219178082192
'''