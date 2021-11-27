from difflib import SequenceMatcher

str1="abcde"
str2=" abce"
s = SequenceMatcher(None, str1, str2)
print(s.get_matching_blocks())
for mb in s.get_matching_blocks():
	print(mb, str1[mb.a:mb.a+mb.size])
	print(mb, str2[mb.b:mb.b+mb.size])

'''
[Match(a=0, b=1, size=3), Match(a=4, b=4, size=1), Match(a=5, b=5, size=0)]
Match(a=0, b=1, size=3) abc
Match(a=0, b=1, size=3) abc
Match(a=4, b=4, size=1) e
Match(a=4, b=4, size=1) e
Match(a=5, b=5, size=0)
Match(a=5, b=5, size=0)
'''