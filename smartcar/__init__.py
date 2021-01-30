from .vehicle_stats import *
from homeassistant import core
from .auth import *
from homeassistant.helpers.typing import HomeAssistantType
from .const import DOMAIN, client
import smartcar

# PLATFORMS = ["auth_client", "vehicle_stats"]

def setup(hass:HomeAssistantType, config):
    """ Setup called when Home Assistant loads the components"""
    # core._async_create_timer(hass)
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

    def login(client:smartcar.AuthClient,hass:HomeAssistantType):
        
        if client == None:
            hass.states.set("smartcar.login","Client not Authenicated") 
            
        auth_url = client.get_auth_url()
        hass.http.register_redirect(client.redirect_uri,auth_url)

    def exchange(call):
        global code
        code = call.data.get('code')
        global access
        access = client.exchange_code(code)
        vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
        hass.states.set("vehicle_ids: ",vehicle_ids)
    
    def veh_wrapper(call):
        data = call.data
        global code
        if not_auth(code):
            perms = permissions(code)
            vehicle_obj = accessVehicle(data, code)
            battery = read_battery(code)
            oil = read_engine_oil(code)
            charge = read_charge(code)
            start = start_charge(code)
            stop = stop_charge(code)
            fuel = read_fuel(code)
            loc = read_location(code)
            odo = read_odometer(code)
            tires = read_tires(code)
            info  = read_vehicle_info(code)
            vin = read_vin(code)
            if data.get("batch",0):
                batch(data, code)
            if data.get("lock",0)!= None or data.get("lock")!=False:
                locked = lock(code)
            if data.get("unlock",0)!= None or data.get("unlock")!=False:
                unlocked = unlock(code)         

        hass.states.set("smartcar.VehicleStats","success")
        disconnect(code)
    # Load/register the platforms we need

    hass.services.register(DOMAIN, 'auth_client', authclient)
    hass.services.register(DOMAIN, 'exchange', exchange)
    hass.services.register(DOMAIN, 'vehicle_stats', veh_wrapper)
    
    #TODO Platforms, refreshToken

    # for component in PLATFORMS:
    #     hass.helpers.discovery.load_platform(component, DOMAIN, {}, config)
    #     hass.services.register(DOMAIN, component+'_service', config)
    return True