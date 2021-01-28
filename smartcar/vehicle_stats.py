from .const import code, jsonify, access
import smartcar

def not_auth(code):
        if code==None:
            return False

def accessVehicle(data,id):
    if id != code:
        return {"status": "Invalid code"}
    global vehicleobj
    vehicleobj = smartcar.Vehicle(data['vehicle_id'], access['access_token'])
    return vehicleobj.info()

def permissions(id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    return jsonify(vehicleobj.permissions())


def batch(call, id):
    if vehicleobj == None:
        return {"status": "No vehicle selected"}
    if id != code:
        return {"status": "Invalid code"}
    data = call.data
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
