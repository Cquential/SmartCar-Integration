""" Platform for the smartcar to authenticate a client and handle backend token stuff
                                                                                  ^  
                                                                                  |
                                                                                (Replace later on)  
"""

import smartcar
from .const import (access, request, redirect, vehicleobj)

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

def login():
    # TODO: Authorization Step 2: Launch Smartcar authentication dialog
    if client == None:
        return {"status": "Client not authenticated"}
    auth_url = client.get_auth_url()
    return redirect(auth_url)

def refreshToken():
    global access
    data = request.get_json()
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
