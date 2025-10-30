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



def plot_sampling_period_hist(time):
    sampling_period = []
for i in range(len(time)-1):
    sampling_periods.append(time[i+1]-time[i])
plt.figure(figsize = (10,6))
plt.hist(sampling_periods)
plt.title("Распределение периодов дискретизации измерений по времени на одно измерение")
plt.xlim(0, 0.06)
plt.grid()
plt.show()