from homeassistant.helpers.typing import HomeAssistantType
from .const import DOMAIN, ATTR_NAME, DEFAULT_NAME,request, client
import smartcar
# import asyncio

PLATFORMS = ["auth_client", "vehicle_stats"]

def setup(hass:HomeAssistantType, config):
    """ Setup called when Home Assistant loads the components"""

    def handle_hello(call):
        """Handle the service call."""
        name = call.data.get(ATTR_NAME, DEFAULT_NAME)
        print(type(call),call)
        hass.states.set("smartcar.hello", name)
    def authclient(call):
        data = call.data # data is a json object pretty much, treat it as a dictionary
        client = smartcar.AuthClient(
                    client_id=data['CLIENT_ID'],
                    client_secret=data['CLIENT_SECRET'],
                    redirect_uri=data['REDIRECT_URI'],
                    scope = data['scope'],
                    test_mode = bool(data['test_mode'])
        )
        login(client,hass)
        hass.states.set("smartcar.authclient", "success")
        # return {"status": "success"}
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

    def authclient():
        data = request.get_json()
        print(type(data),data)
        # global client
        client = smartcar.AuthClient(
                    client_id=data['CLIENT_ID'],
                    client_secret=data['CLIENT_SECRET'],
                    redirect_uri=data['REDIRECT_URI'],
                    scope = data['scope'],
                    test_mode = bool(data['test_mode'])
        )
        return {"status": "success"}

    def login(client:smartcar.AuthClient,hass:HomeAssistantType):
        # TODO: Authorization Step 2: Launch Smartcar authentication dialog
        if client == None:
            hass.states.set("smartcar.login","Client not Authenicated") 
            # return {"status": "Client not authenticated"}
        auth_url = client.get_auth_url()
        try: 
            hass.http.register_redirect('https://google.com',client.redirect_uri)
        except:
            print('garbage', client.redirect_uri)
        hass.http.register_redirect('',auth_url)

    def exchange():
        global code
        code = request.args.get('code')
        global access
        access = client.exchange_code(code)
        vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
        return {"vehicle_ids": vehicle_ids}

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


    # Load/register the platforms we need
    hass.services.register(DOMAIN, 'hello', handle_hello)
    hass.services.register(DOMAIN, 'auth_client', authclient)
    # for component in PLATFORMS:
    #     hass.helpers.discovery.load_platform(component, DOMAIN, {}, config)
    #     hass.services.register(DOMAIN, component+'_service', config)
    return True