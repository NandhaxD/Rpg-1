from Sylvie import *
from Sylvie.Database import *

def get_location(loc_id):
    location = locations.get(loc_id)
    if location:
        return location
    else:
        return False
