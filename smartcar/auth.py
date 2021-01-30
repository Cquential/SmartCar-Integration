import homeassistant
from .const import access, vehicleobj, code
import smartcar

def refreshToken(call):
    global access
    data = call.data
    if data["current_token"] == access['refresh_token']:
        access = client.exchange_refresh_token(access['refresh_token'])
        return {"status": "refreshed"}
    return {"status": "token mismatch"}

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