import psutil
import matplotlib.pyplot as plt
import time

cpu_data = []

for i in range(10):
    cpu = psutil.cpu_percent(interval=1)
    cpu_data.append(cpu)
    print(f"CPU: {cpu}%")

plt.plot(cpu_data)
plt.title("CPU Usage Over Time")
plt.xlabel("Time")
plt.ylabel("CPU %")
plt.show()