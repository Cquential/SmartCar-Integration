from flask import jsonify

DOMAIN = "smartcar"
ATTR_NAME = "name"
DEFAULT_NAME = "CAR"

code = None
access = None
vehicleobj = None
client = None