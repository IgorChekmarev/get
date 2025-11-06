import smbus
import time
class MCP3021:
    def __init__(self, dynamic_range, verbose = False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        if self.verbose:
            print(f"Принятые данные: {data}, старший байт: {upper_data_byte:x}, младший байт: {lower_data_byte:x}, число: {number}")
        return number

    def get_voltage(self):
        number = self.get_number()
        voltage = (number/649)*self.dynamic_range
        return voltage


if __name__ == "__main__":
    try:
        adc = MCP3021(dynamic_range=3.278, verbose = True)

        print("Измерение напряжения MCP3021")

        while True:
            voltage = adc.get_voltage()
            print(f"Измеренное напряжение: {voltage: .3f} B")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nИзмерение прервано")

    finally:
        adc.deinit()