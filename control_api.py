from flask import Flask, render_template, request
from pyfirmata import ArduinoMega, util
import time

app = Flask(__name__)

board = ArduinoMega('COM5')

it = util.Iterator(board)
it.start()

led = board.get_pin('d:4:o')  # LED
fan = board.get_pin('d:32:o')  # fen
water = board.get_pin('d:9:o')  # water pump


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/run_code', methods=['POST'])
def run_code():
    data = request.form.get('data')
    part = data.split("_")[0]
    onoff = data.split("_")[1]
    if onoff == "on":
        onoff = 1
    else:
        onoff = 0

    if part == "led":
        part = led
    elif part == "fan":
        part = fan
    else:
        part = water

    part.write(onoff)

    result = f"눌린 버튼: {data}"
    return result


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':
    main()
