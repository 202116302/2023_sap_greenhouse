import time
from datetime import datetime
import urllib.request
import smbus
import RPi.GPIO as GPIO
import board
import adafruit_dht
from urllib.error import URLError
import LCD1602

# pin = 4

dhtDevice = adafruit_dht.DHT22(board.D4)
LCD1602.init(0x27, 1)


# lux

DEVICE = 0x23  # Default device I2C address

POWER_DOWN = 0x00  # No active state

POWER_ON = 0x01  # Power on

RESET = 0x07  # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.

CONTINUOUS_LOW_RES_MODE = 0x13

# Start measurement at 1lx resolution. Time typically 120ms

CONTINUOUS_HIGH_RES_MODE_1 = 0x10

# Start measurement at 0.5lx resolution. Time typically 120ms

CONTINUOUS_HIGH_RES_MODE_2 = 0x11

# Start measurement at 1lx resolution. Time typically 120ms

# Device is automatically set to Power Down after measurement.

ONE_TIME_HIGH_RES_MODE_1 = 0x20

# Start measurement at 0.5lx resolution. Time typically 120ms

# Device is automatically set to Power Down after measurement.

ONE_TIME_HIGH_RES_MODE_2 = 0x21

# Start measurement at 1lx resolution. Time typically 120ms

# Device is automatically set to Power Down after measurement.

ONE_TIME_LOW_RES_MODE = 0x23

# bus = smbus.SMBus(0) # Rev 1 Pi uses 0

bus = smbus.SMBus(1)  # Rev 2 Pi uses 1


def convertToNumber(data):
    # Simple function to convert 2 bytes of data

    # into a decimal number

    return ((data[1] + (256 * data[0])) / 1.2)


def readLight(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)

    return convertToNumber(data)


while True:
    try:
        now = datetime.now()
        t = dhtDevice.temperature
        h = dhtDevice.humidity

        if h is not None and t is not None:
            print(
                "Temperature = {:0.1f}℃ Humidity = {:0.1f}% Light Level = {:0.1f}lx Time = {}".format(t, h, readLight(),
                                                                                                      now.strftime(
                                                                                                          '%H:%M:%S %m-%d')))
            LCD1602.write(2, 0, '{:0.1f}C {:0.1f}%'.format(t, h))
            LCD1602.write(5, 1, '{:0.1f}lx'.format(readLight()))
            time.sleep(3)
            # html = urllib.request.urlopen(
            #     "https://api.thingspeak.com/update?api_key=W0PHS3YGBJ8GSKQJ&field1={:0.1f}&field2={:0.1f}&field3={:0.1f}".format(
            #         t, h, readLight()))
        else:
            time.sleep(3)
            print('Read error')

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue

    except URLError as e:
        print(e.args[0])
        time.sleep(2.0)
        continue

    except OSError as e:
        print(e.args[0])
        time.sleep(5)
        continue


    except KeyboardInterrupt:
        print("Terminated by Keyboard")
        break
