def isdigit(str_):
    print(str_, str_.isdigit())
    return str_.isdigit()


if __name__ == "__main__":
    isdigit("1200")
    isdigit(" 1200")
    isdigit(" 1200 ")
    isdigit("+1200")
    isdigit("-1200")
    isdigit("12.3")
    isdigit("a12")
    isdigit("12A")
    isdigit("12e1")
    isdigit("120000000000000000000000000000000000000000000000000000000000")
    isdigit("000000000000000000000000000000000000000000000000000000000012")


'''
1200 True
 1200 False
 1200  False
+1200 False
-1200 False
12.3 False
a12 False
12A False
12e1 False
120000000000000000000000000000000000000000000000000000000000 True
000000000000000000000000000000000000000000000000000000000012 True
'''