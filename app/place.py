import json

class Place:
    def __init__(self, place_id, name, business_status, is_open, secondary_opening_hours, current_opening_hours, delivery, dine_in, editorial_summary, location, vicinity, formatted_address, adr_address, rating, user_ratings_total, reviews):
        self.place_id = place_id
        self.name = name
        self.business_status = business_status
        self.is_open = is_open
        self.secondary_opening_hours = secondary_opening_hours
        self.current_opening_hours = current_opening_hours
        self.delivery = delivery
        self.dine_in = dine_in
        self.editorial_summary = editorial_summary
        self.location = location
        self.vicinity = vicinity
        self.formatted_address = formatted_address
        self.adr_address = adr_address
        self.rating = rating
        self.user_ratings_total = user_ratings_total
        self.reviews = reviews
        self.is_near = True
    
    def to_dict(self):
        return self.__dict__