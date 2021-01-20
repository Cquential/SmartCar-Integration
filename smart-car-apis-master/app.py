import smartcar
import json
from flask import Flask, request, redirect, jsonify

code = None
access = None
vehicleobj = None
client = None

app = Flask(__name__)


@app.route('/authclient', methods=['POST'])
def authclient():
    data = request.get_json()
    print(type(data),data)
    global client
    client = smartcar.AuthClient(
                client_id=data['CLIENT_ID'],
                client_secret=data['CLIENT_SECRET'],
                redirect_uri=data['REDIRECT_URI'],
                scope = data['scope'],
                test_mode = bool(data['test_mode'])
    )
    return {"status": "success"}


@app.route('/login', methods=['GET'])
def login():
    # TODO: Authorization Step 2: Launch Smartcar authentication dialog
    if client == None:
        return {"status": "Client not authenticated"}
    auth_url = client.get_auth_url()
    return redirect(auth_url)


@app.route('/exchange', methods=['GET'])
def exchange():
    global code
    code = request.args.get('code')
    global access
    access = client.exchange_code(code)
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    return {"vehicle_ids": vehicle_ids}


@app.route('/refreshToken', methods=['POST'])
def refreshToken():
    global access
    data = request.get_json()
    if data["current_token"] == access['refresh_token']:
        access = client.exchange_refresh_token(access['refresh_token'])
        return {"status": "refreshed"}
    return {"status": "token mismatch"}


@app.route('/checkCompatiblity', methods=['POST'])
def checkCompatible():
    data = request.get_json()
    return {"status": client.is_compatible(data["vin"], data["scope"], country=data["country"])}


@app.route('/v1.0/vehicles/<string:id>/accessVehicle', methods=['POST'])
def accessVehicle(id):
    if id != code:
        return {"status": "Invalid code"}
    global vehicleobj
    data = request.get_json()
    vehicleobj = smartcar.Vehicle(data['vehicle_id'], access['access_token'])
    return vehicleobj.info()


@app.route('/v1.0/vehicles/<string:id>/permissions')
def permissions(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return jsonify(vehicleobj.permissions())


@app.route('/v1.0/vehicles/<string:id>/batch', methods=['POST'])
def batch(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    data = request.get_json()
    return vehicleobj.batch(data['batch'])


@app.route('/v1.0/vehicles/<string:id>/application', methods = ['DELETE'])
def disconnect(id):
    global code, access, vehicleobj, client
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    vehicleobj.disconnect()
    code = None
    access = None
    vehicleobj = None
    client = None
    return {"status": "Disconnected"}


@app.route('/v1.0/vehicles/<string:id>/engine/oil')
def read_engine_oil(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.oil()


@app.route('/v1.0/vehicles/<string:id>/battery')
def read_battery(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.battery()


@app.route('/v1.0/vehicles/<string:id>/charge')
def read_charge(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.charge()


@app.route('/v1.0/vehicles/<string:id>/startcharge', methods = ['POST'])
def start_charge(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.start_charge()


@app.route('/v1.0/vehicles/<string:id>/stopcharge', methods = ['POST'])
def stop_charge(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.stop_charge()


@app.route('/v1.0/vehicles/<string:id>/fuel')
def read_fuel(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.fuel()


@app.route('/v1.0/vehicles/<string:id>/location')
def read_location(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.location()


@app.route('/v1.0/vehicles/<string:id>/lock', methods = ['POST'])
def lock(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.lock()


@app.route('/v1.0/vehicles/<string:id>/unlock', methods = ['POST'])
def unlock(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.unlock()


@app.route('/v1.0/vehicles/<string:id>/odometer')
def read_odometer(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.odometer()


@app.route('/v1.0/vehicles/<string:id>/tires/pressure')
def read_tires(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.tirePressure()


@app.route('/v1.0/vehicles/<string:id>/user')
def get_user(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return smartcar.get_user_id(access['access_token'])


@app.route('/v1.0/vehicles/<string:id>')
def read_vehicle_info(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.info()


@app.route('/v1.0/vehicles/<string:id>/vin')
def read_vin(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.vin()


app.run(port = 8000, debug = True)
