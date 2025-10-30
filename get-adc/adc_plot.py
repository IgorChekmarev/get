from matplotlib import pyplot
def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize = (10, 6))
    plt.plot(time, voltage)
    plt.xlabel("time, sec")
    plt.ylabel("voltage, V")
    plt.title("Voltage VS time plot")
    plt.show()