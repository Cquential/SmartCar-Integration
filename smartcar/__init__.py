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
        print(type(data),data)
        # global client
        client = smartcar.AuthClient(
                    client_id=data['CLIENT_ID'],
                    client_secret=data['CLIENT_SECRET'],
                    redirect_uri=data['REDIRECT_URI'],
                    scope = data['scope'],
                    test_mode = bool(data['test_mode'])
        )
        hass.states.set("smartcar.authclient", "success")
        # return {"status": "success"}

    # Load/register the platforms we need
    hass.services.register(DOMAIN, 'hello', handle_hello)
    hass.services.register(DOMAIN, 'auth_client', authclient)
    for component in PLATFORMS:
        hass.helpers.discovery.load_platform(component, DOMAIN, {}, config)
        hass.services.register(DOMAIN, component+'_service', config)
    return True
