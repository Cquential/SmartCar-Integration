from config.custom_components.smartcar.vehicle_stats import accessVehicle, not_auth
from homeassistant import core
from .auth import *
# from .vehicle_stats import veh_wrapper
from homeassistant.helpers.typing import HomeAssistantType
from .const import DOMAIN, ATTR_NAME, DEFAULT_NAME,request, client, jsonify
import smartcar
# import asyncio

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
            vehicle_obj = accessVehicle(data, code)

        hass.states.set("smartcar.VehicleStats","Electric Boogaloo")

    # Load/register the platforms we need

    hass.services.register(DOMAIN, 'auth_client', authclient)
    hass.services.register(DOMAIN, 'exchange', exchange)
    hass.services.register(DOMAIN, 'vehicle_stats', veh_wrapper)
    
    #TODO Platforms!!!
    # for component in PLATFORMS:
    #     hass.helpers.discovery.load_platform(component, DOMAIN, {}, config)
    #     hass.services.register(DOMAIN, component+'_service', config)
    return True