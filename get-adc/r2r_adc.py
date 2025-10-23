
import RPi.GPIO as GPIO
import time

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


if __name__ == "__main__":
    try:
        adc = R2R_ADC(dynamic_range=3.278, compare_time=0.01, verbose=True)
        
        print("АЦП запущен. Для остановки нажмите Ctrl+C")
        
        while True:
            voltage = adc.get_sc_voltage()
            print(f"Измеренное напряжение: {voltage:.3f} В")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nИзмерение прервано")
    finally:
        adc.deinit()