from time import sleep_ms

class I2cLcd:

    def __init__(self, i2c, addr, rows, cols):

        self.i2c = i2c
        self.addr = addr

        sleep_ms(20)

        self.write_cmd(0x33)
        self.write_cmd(0x32)
        self.write_cmd(0x28)
        self.write_cmd(0x0C)
        self.write_cmd(0x06)
        self.write_cmd(0x01)

        sleep_ms(5)

    def lcd_write(self, data):

        self.i2c.writeto(self.addr, bytes([data | 0x08]))

    def pulse_enable(self, data):

        self.lcd_write(data | 0x04)

        sleep_ms(1)

        self.lcd_write(data & ~0x04)

        sleep_ms(1)

    def write4bits(self, data):

        self.lcd_write(data)

        self.pulse_enable(data)

    def write_cmd(self, cmd):

        self.write4bits(cmd & 0xF0)

        self.write4bits((cmd << 4) & 0xF0)

    def write_data(self, data):

        self.write4bits((data & 0xF0) | 0x01)

        self.write4bits(((data << 4) & 0xF0) | 0x01)

    def clear(self):

        self.write_cmd(0x01)

        sleep_ms(2)

    def move_to(self, col, row):

        addr = col + (0x40 * row)

        self.write_cmd(0x80 | addr)

    def putstr(self, string):

        for char in string:

            self.write_data(ord(char))