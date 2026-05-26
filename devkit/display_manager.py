from machine import Pin, SoftI2C

from i2c_lcd import I2cLcd

# ======================================
# I2C
# ======================================

i2c = SoftI2C(

    scl=Pin(22),

    sda=Pin(21),

    freq=400000

)

# ======================================
# LCD
# ======================================

lcd = I2cLcd(

    i2c,

    0x3F,

    2,

    16

)

# ======================================
# SHOW
# ======================================

def show(

    line1="",

    line2=""

):

    lcd.clear()

    lcd.move_to(0, 0)

    lcd.putstr(line1[:16])

    lcd.move_to(0, 1)

    lcd.putstr(line2[:16])