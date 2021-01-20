""" Platform for vehicle stats """

from .const import (code, vehicleobj, request, 
 redirect, jsonify, access, client
)
import asyncio, smartcar

def not_auth():
    pass

def accessVehicle(id):
    if id != code:
        return {"status": "Invalid code"}
    global vehicleobj
    data = request.get_json()
    vehicleobj = smartcar.Vehicle(data['vehicle_id'], access['access_token'])
    return vehicleobj.info()
