import matplotlib.pyplot as plt
#https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.pyplot.scatter.html

x = [ x for x in range(0,3)]
plt.scatter(x,x,c=x)
plt.show()

x = [ x for x in range(100,110)]
plt.scatter(x,x,c=x)
plt.show()
