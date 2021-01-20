""" Platform for vehicle stats """

from .const import (code, vehicleobj, request, 
 redirect, jsonify, access, client
)
import asyncio, smartcar

def exchange():
    global code
    code = request.args.get('code')
    global access
    access = client.exchange_code(code)
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    return {"vehicle_ids": vehicle_ids}

def not_auth():
    if code==None:
        return {"status":"not logged in"}

def accessVehicle(id):
    if id != code:
        return {"status": "Invalid code"}
    global vehicleobj
    data = request.get_json()
    vehicleobj = smartcar.Vehicle(data['vehicle_id'], access['access_token'])
    return vehicleobj.info()
def permissions(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return jsonify(vehicleobj.permissions())

def batch(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    data = request.get_json()
    return vehicleobj.batch(data['batch'])

def read_battery(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.battery()

def read_engine_oil(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.oil()

def read_charge(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.charge()

def start_charge(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.start_charge()

def stop_charge(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.stop_charge()

def read_fuel(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.fuel()

def read_location(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.location()

def lock(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.lock()

def unlock(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.unlock()

def read_odometer(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.odometer()

def read_tires(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.tirePressure()

def get_user(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return smartcar.get_user_id(access['access_token'])

def read_vehicle_info(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.info()

def read_vin(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return vehicleobj.vin()

