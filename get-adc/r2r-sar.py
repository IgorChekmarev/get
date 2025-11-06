import RPi.GPIO as GPIO
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

def plot_sampling_period_hist(t):
    sampling_periods = []
    for i in range(len(t)-1):
        sampling_periods.append(t[i+1]-t[i])
    plt.figure(figsize = (10,6))
    plt.hist(sampling_periods)
    plt.title("Распределение периодов дискретизации измерений по времени на одно измерение")
    plt.xlim(0, 0.6)
    plt.grid()
    plt.show()

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.000000001, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def dec2bin(self, value):
        return [int(element) for element in bin(value)[2:].zfill(8)]

    def number_to_dac(self, number):
        for i in range(8):
            GPIO.output(self.bits_gpio[i], (self.dec2bin(number))[i])

        
        if self.verbose:
            print(f"Подано число: {number} (бинарно: {self.dec2bin(number)})")

    def sequential_counting_adc(self):
        max_value = 2**len(self.bits_gpio) - 1
        
        for number in range(max_value + 1):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            comparator_state = GPIO.input(self.comp_gpio)
            
            if self.verbose:
                print(f"Число: {number}, Компаратор: {comparator_state}")
            
            if comparator_state == 1:
                return number
        
        return max_value

    def get_sc_voltage(self):
        digital_value = self.sequential_counting_adc()
        max_digital_value = 2**len(self.bits_gpio) - 1
        voltage = (digital_value / max_digital_value) * self.dynamic_range
        
        if self.verbose:
            print(f"Цифровое значение: {digital_value}, Напряжение: {voltage:.3f} В")
        
        return voltage

    def successive_approximation_adc(self):
        low = 0
        high = 255
        result = 0
        for i in range(8):
            med = (low + high)//2
            self.number_to_dac(med)
            time.sleep(self.compare_time)


            comp = GPIO.input(self.comp_gpio)
            if comp == 1:
                high = med+1
                result = med
            else:
                low = med-1
        print(result)
        return result

    def get_sar_voltage(self):
        value = self.successive_approximation_adc()
        return value*self.dynamic_range/255

voltage_values = []
time_values = []
duration = 3.0

if __name__ == "__main__":
    try:
        adc = R2R_ADC(dynamic_range=3.278, verbose=True)
        time_start = time.time()
        
        while (time.time() - time_start)<duration:
            voltage = adc.get_sar_voltage()
            print(f"Измеренное напряжение: {voltage:.3f} В")
            voltage_values.append(adc.get_sar_voltage())
            print(voltage_values)
            time_values.append(time.time() - time_start)
            print(time_values)

        plot_voltage_vs_time(time_values, voltage_values, 3.28, duration)
        plot_sampling_period_hist(time_values)
        print(time_values)
        print(voltage_values)
    except KeyboardInterrupt:
        print("\nИзмерение прервано")
    finally:
        adc.deinit()
