import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.wm = 0x00
        self.pds = 0x00
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return

        if not (0 <= number <= 4095):
            print("Число выходит за разрядность МСР4725 (12 бит)")
            return

        first_byte = self.wm | self.pds | (number >> 8)
        second_byte = number & 0xFF
        self.bus.write_byte_data(self.address, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f}) В")
            return
        
        # Преобразуем напряжение в цифровое значение (12 бит)
        # voltage / dynamic_range = number / 4095
        number = int((voltage / self.dynamic_range) * 4095)
        
        # Ограничиваем значение 12 битами
        number = max(0, min(number, 4095))
        
        # Устанавливаем значение через set_number
        self.set_number(number)
        
        if self.verbose:
            print(f"Установлено напряжение: {voltage:.2f} В, цифровое значение: {number}")

if __name__ == "__main__":
    try:
        # Создаем объект MCP4725 вместо PWM_DAC
        dac = MCP4725(dynamic_range=3.28, address=0x61, verbose=True)
        while True:
            try:
                user_input = input("Введите напряжение в вольтах: ").strip().replace(',', '.')
                voltage = float(user_input)
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac.deinit()