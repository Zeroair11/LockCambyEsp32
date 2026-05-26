from machine import Pin
import time

KEYS = [
    ["1","2","3","A"],
    ["4","5","6","B"],
    ["7","8","9","C"],
    ["*","0","#","D"]
]

class Keypad:

    def __init__(self, row_pins, col_pins):

        self.rows = [Pin(p, Pin.OUT) for p in row_pins]
        self.cols = [Pin(p, Pin.IN, Pin.PULL_UP) for p in col_pins]

        for r in self.rows:
            r.value(1)

    def scan(self):

        for i, r in enumerate(self.rows):

            r.value(0)

            for j, c in enumerate(self.cols):

                if c.value() == 0:

                    time.sleep_ms(20)

                    if c.value() == 0:

                        r.value(1)

                        return KEYS[i][j]

            r.value(1)

        return None