from pyfirmata import ArduinoMega, util
import time
import numpy as np


board = ArduinoMega('COM5')

it = util.Iterator(board)
it.start()
led = board.get_pin('d:4:o') # LED
fen = board.get_pin('d:32:o') # fen
red = board.get_pin('d:23:o') # mini led red
water = board.get_pin('d:9:o') # water pump
led_index = 0

while True:
    # led.write(led_index % 2) # LED write 1 켜짐 0 꺼짐
    # fen.write((led_index // 3) % 2)
    # led_index += 1

    water.write(0)
    time.sleep(2)
    water.write(0)
    time.sleep(10)