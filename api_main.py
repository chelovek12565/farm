from flask import Flask, jsonify, request

app = Flask(__name__)
data = {
    'light': 8000,
    'temp': 20,
    'vent': True
}


@app.route('/all', methods=['GET'])
def return_all_data():
    global data
    return jsonify({
        'light': data['light'],
        'temp': data['temp'],
        'vent': data['vent']
    })


@app.route('/send_command')
def send_command():
    command = request.json['command']
    # TODO do_something


@app.route('/api/temperature', methods=['PUT'])
def temperature():
    data['temp'] = request.json['temp']


app.run()