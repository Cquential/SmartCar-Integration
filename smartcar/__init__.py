from .const import DOMAIN, ATTR_NAME, DEFAULT_NAME

def setup(hass, config):
    """ Setup called when Home Assistant loads the components"""
    
    def handle_hello(call):
        """Handle the service call."""
        name = call.data.get(ATTR_NAME, DEFAULT_NAME)

        hass.states.set("smartcar.hello", name)

    hass.services.register(DOMAIN, "hello", handle_hello)
    return True
