print(__file__,"start")
import main2
print("in import2(main.value)",main2.value)
main2.value = 20
print("in import2(main.value)",main2.value)
print(__file__,"end")