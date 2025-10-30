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

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
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

voltage_values = []
time_values = []
duration = 3.0

if __name__ == "__main__":
    try:
        adc = R2R_ADC(dynamic_range=3.278, compare_time=0.01, verbose=True)
        time_start = time.time()
        
        while (time.time() - time_start)<duration:
            voltage = adc.get_sc_voltage()
            print(f"Измеренное напряжение: {voltage:.3f} В")
            voltage_values.append(adc.get_sc_voltage())
            print(voltage_values)
            time_values.append(time.time() - time_start)
            print(time_values)

        plot_voltage_vs_time(time_values, voltage_values, 3.28, duration)
        print(time_values)
        print(voltage_values)
    except KeyboardInterrupt:
        print("\nИзмерение прервано")
    finally:
        adc.deinit()
