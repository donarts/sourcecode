import math
import matplotlib.pyplot as plt
import numpy as np

time_step_size = 5
timed_y_list = []
x_list = []
y_list = []
for xx in range(0, 14400, 1):
    x = xx/1000.0
    y = 2.0 * math.sin(x) + math.sin(2.0*x)+math.sin(6.0*x)+math.cos(x) + 4.0
    timed_y_list.append(y)

timed_y_data = np.array(timed_y_list)
print(timed_y_data)
np.savetxt("timed_y_data.csv", timed_y_data, delimiter=',')

for xx in range(len(timed_y_list)-time_step_size):
    x_list.append(timed_y_list[xx:xx+time_step_size])
    y_list.append(timed_y_list[xx+time_step_size])

x_np = np.array(x_list)
y_np = np.array(y_list)
print(x_np)
print(y_np)

np.savetxt("x_data.csv", x_np, delimiter=',')
np.savetxt("y_data.csv", y_np, delimiter=',')


fig, ax = plt.subplots()
ax.plot(timed_y_data)
plt.savefig("timed_y_data.png")
