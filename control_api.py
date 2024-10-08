from flask import Flask, render_template, request, jsonify
from pyfirmata import ArduinoMega, util
import time

from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app, resources={r'*': {'origins': '*'}})

board = ArduinoMega('/dev/ttyACM0')

it = util.Iterator(board)
it.start()

led = board.get_pin('d:4:o')  # LED
fan = board.get_pin('d:32:o')  # fen
water = board.get_pin('d:9:o')  # water pump


@app.route('/index.html')
def home():
    return render_template('index.html')


@app.route('/run_code', methods=['POST'])


def run_code():
    # data = request.form.get('data')
    # part = data.split("_")[0]
    # onoff = data.split("_")[1]
    # if onoff == "on":
    #     onoff = 1
    # else:
    #     onoff = 0

    # if part == "led":
    #     part = led
    # elif part == "fan":
    #     part = fan
    # else:
    #     part = water

    # part.write(onoff)

    data = request.get_json()
    received_data = data.get('data')
    print(data)
    print(received_data)
    part = received_data.split("_")[0]
    onoff = received_data.split("_")[1]
    if onoff == "on":
        onoff = 1
    elif onoff == "off":
        onoff = 0
    else:
        pass

    if part == "led":
        part = led
    elif part == "leed":
        part = led
    elif part == "fan":
        part = fan
    elif part == "water":
        part = water
    else:
        pass

    part.write(onoff)


    return jsonify(data)



def main():
    app.run(host="0.0.0.0", port=8000)


if __name__ == '__main__':
    main()
