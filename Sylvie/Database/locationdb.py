from Sylvie import db

def get_location(loc_id):
    location = db.location.find_one({"location_id": loc_id})
    if location:
        return location
    else:
        return False
