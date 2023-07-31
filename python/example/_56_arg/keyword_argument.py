


print(complex(real=1, imag=2))
# (1+2j)

print(complex(imag=2))
# 2j

print(complex(real=1))
# (1+0j)

print("## 1 ##")
com_data = [[1, 2], [0, 2], [1, 0]]
for one in com_data:
    print(complex(one[0], one[1]))

print("## 2 ##")
com_data = [{"real": 1, "imag": 2}, {"real": 0, "imag": 2}, {"real": 1, "imag": 0}]
for one in com_data:
    print(complex(one.get("real"), one.get("imag")))

print("## 3 ##")
com_data = [{"real": 1, "imag": 2}, {"imag": 2}, {"real": 1}]
for one in com_data:
    print(complex(**one))
