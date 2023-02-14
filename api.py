from flask import Flask, request

# import os
from pprint import pprint
import googlemaps #pip install googlemaps

app = Flask(__name__)
app.config["DEBUG"] = True

API_KEY = open('API_KEY.txt').read()
map_client = googlemaps.Client(API_KEY)

def miles_to_meters(miles):
    try:
        print('Meters', miles * 1.609,344)
        return miles * 1.609,344
    except:
        return 0

def get_place_info(location, distance):
    try: 
        response = map_client.places_nearby(
            type='restaurant|pharmacy', #type=food
            location=location,
            radius = distance,
        )
        results = response.get('results')
        print("Termine")
        return results
    except Exception as e:
        print(e)
        return None

@app.route('/', methods=['GET'])
def home():
    return "El servidor está inicializado en el puerto ????"
    
@app.route('/stores/near', methods=['GET'])
def storesNearby():
    latitud = request.args.get('latitud')
    longitud = request.args.get('longitud')
    # location = ('-34.8764965,-56.0947794')
    location = (latitud,longitud)
    distance = miles_to_meters(800)
    return get_place_info(location, distance)

app.run()