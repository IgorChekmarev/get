import smbus
class MCP4725:
    def __init__(self, dynamic_range, addres=0x61, verbose = True):
        self.bus = smbus.SMBus(1)
        self.addres = addres
        self.wm = 0x00
        self.pds = 0x00
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")

        if not (0<= number <= 4095):
            print("Число выходит за разрядность МСР4725 (12 бит)")

        first_byte = self.wm | self.pds | number >> 8
        second_byte = number & 0xFF
        self.bus.write_byte_data(0x61, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.addres << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")

    def set_voltage(self, voltage):
        









if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.28, True)
        while True:
            try:
                user_input = input("Введите напряжение в вольтах: ")
                voltage = float(user_input)
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac.deinit()