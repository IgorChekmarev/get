import time
from matplotlib import pyplot as plt
def plot_voltage_vs_time(time, voltage, max_voltage, duration):
    plt.figure(figsize = (10, 6))
    plt.plot(time, voltage)
    plt.ylim(0, max_voltage + 0.5)
    plt.xlim(0, duration)
    plt.xlabel("time, sec")
    plt.ylabel("voltage, V")
    plt.title("Voltage VS time plot")
    plt.grid()
    plt.show()
time_values = []
voltage_values = []
duration = 3.0
current_time = 0
while current_time <duration:
    current_time = time.time() - 0
    time_values.append(float(current_time))
    voltage_values.append(float(1))

    print(time.time())
plot_voltage_vs_time(time_values, voltage_values, 3.28, duration)
print(time_values, voltage_values)