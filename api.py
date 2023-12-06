import json
from flask import Flask, request

# import os
import time
from pprint import pprint
import googlemaps #pip install googlemaps
from app.place import Place
from utils import miles_to_meters

app = Flask(__name__)
app.config["DEBUG"] = False

API_KEY = open('API_KEY.txt').read()
map_client = googlemaps.Client(API_KEY)


def parse_data(arrayPlaces):
    data = []
    try:
        print("len(arrayPlaces)", len(arrayPlaces))
        for i in range(0,len(arrayPlaces)):
            print("(i)", i)
            currentPlace = arrayPlaces[i]

            place_id = currentPlace['place_id'] if ('place_id' in currentPlace) else None
            print("1 place_id", place_id)
            name = currentPlace['name'] if ('name' in currentPlace) else None
            print("2 Name", name)
            business_status = currentPlace['business_status'] if ('business_status' in currentPlace) else None
            print("3 Business_status", business_status)
            opening_hours = currentPlace['opening_hours'] if ('opening_hours' in currentPlace) else None
            print("4 opening_hours", opening_hours)
            is_open = opening_hours['open_now'] if (opening_hours is not None and 'open_now' in opening_hours) else True
            print("4b is_open", is_open)
            secondary_opening_hours = currentPlace['secondary_opening_hours'] if ('secondary_opening_hours' in currentPlace) else None
            print("4b secondary_opening_hours", secondary_opening_hours)

            current_opening_hours = currentPlace['current_opening_hours'] if ('current_opening_hours' in currentPlace) else None
            print("5 current_opening_hours", current_opening_hours)
            delivery = currentPlace['delivery'] if ('delivery' in currentPlace) else None
            print("6 delivery", delivery)
            dine_in = currentPlace['dine_in'] if ('dine_in' in currentPlace) else None
            print("7 dine_in", dine_in)
            editorial_summary = currentPlace['editorial_summary'] if ('editorial_summary' in currentPlace) else None
            print("8 editorial_summary", editorial_summary)
            geometry = currentPlace['geometry'] if ('geometry' in currentPlace) else None
            print("geometry", geometry)
            location = geometry['location'] if ('location' in geometry) else None
            print("9 location", location)
            vicinity = currentPlace['vicinity'] if ('vicinity' in currentPlace) else None
            print("vicinity", vicinity)
            formatted_address = currentPlace['formatted_address'] if ('formatted_address' in currentPlace) else None
            print("10 formatted_address", formatted_address)
            adr_address = currentPlace['adr_address'] if ('adr_address' in currentPlace) else None
            print('adr_address', adr_address)
            rating = currentPlace['rating'] if ('rating' in currentPlace) else 0
            user_ratings_total = currentPlace['user_ratings_total'] if ('user_ratings_total' in currentPlace) else 0
            print("user_ratings_total", user_ratings_total)
            reviews = currentPlace['reviews'] if ('reviews' in currentPlace) else 0
            print("reviews", reviews)
            place = Place(place_id,
                name,
                business_status,
                is_open,
                secondary_opening_hours,
                current_opening_hours,
                delivery,
                dine_in,
                editorial_summary,
                location,
                vicinity,
                formatted_address,
                adr_address,
                rating,
                user_ratings_total,
                reviews
                )

            jsonData = json.dumps(place.__dict__)
            data.append(json.loads(jsonData))
        return data
    except Exception as e:
        return None

def get_stores(location, rankBy = None, distance = None, nextPage = None, isFirstTime = False, type = "", keyword=""):
    try:
        print("Get Bars \n\n\n")
        # location = ('-34.8764965,-56.0947794')
        response = {}
        stores_list = []

        if nextPage is None:
            print('***************************')
            print('Entro sin Next page', nextPage)
            print('***************************\n')
            if isFirstTime is not True:
                time.sleep(2)

            args = { 'location': location }
            if type != "":
                args['type'] = type
            if keyword != "":
                args['keyword'] = keyword
            if rankBy == "prominence":
                args['radius'] = distance
            else:
                args['rank_by'] = rankBy
            response = map_client.places_nearby(**args)

            print('STATUS', response.get('status'))
            if response.get('status') == "OK":
                stores_list.extend(response.get('results'))
            else:
                print('Error: Algunas tiendas no fueron cargadas')
            print('Final Entro sin Next page')
        else:
            print('\n\n')
            print('***************************')
            print('Entro con Next page ***' + nextPage + '***')
            print('***************************')
            time.sleep(2)
            args = { 'location': location, 'page_token': nextPage }

            response = map_client.places_nearby(**args)

            print('STATUS', response.get('status'))
            if response.get('status') == "OK":
                stores_list.extend(response.get('results'))
            else:
                print('Error: Algunas tiendas no fueron cargadas')
            print('Deberia llegar')

        if(response.get('status') == "OK" and response.get('next_page_token')):
            # print('Next Token result')
            # print(response.get('results'))
            # print("$$$$$ Hay Nueva Pagina ^^^^^", response.get('next_page_token') )
            stores_list.extend(get_stores(location, rankBy, distance, response.get('next_page_token'), type))
            # response = response.get('results') + get_bares(location, distance, response.get('next_page_token'))
        else:
            print('Error: Algunas tiendas no fueron cargadas')
            print('response.get(status)', response.get('status'))

        return stores_list
    except Exception as e:
        print(e)
        return None

def get_footballFields(location, rankBy = None, distance = None, nextPage = None, isFirstTime = False):
    print("Get Football Fields \n\n\n")
    return get_stores(location, rankBy, distance, nextPage, isFirstTime, type = None, keyword="Futbol 5")

def get_bares(location, rankBy = None, distance = None, nextPage = None, isFirstTime = False):
    print("Get Bars \n\n\n")
    return get_stores(location, rankBy, distance, nextPage, isFirstTime, type = "restaurant")

def get_pharmacies(location, rankBy = None, distance = None, nextPage = None, isFirstTime = False):
    print("Get Pharmacies \n\n\n")
    return get_stores(location, rankBy, distance, nextPage, isFirstTime, type = "pharmacy")

def get_place_info(location, rankBy, distance):
    try:
        print("Start")
        # location = ('-34.8764965,-56.0947794')
        # get the start time
        st = time.time()
        bares = get_bares(location, rankBy, distance, None, True)
        # get the end time
        et = time.time()
        st2 = time.time()
        farmacias = get_pharmacies(location, rankBy, distance, None, True)
        et2 = time.time()

        elapsed_time = et - st
        elapsed_time2 = et2 - st2

        results = parse_data(bares + farmacias)
        response = { "stores": results, "size": len(results), "timeLoadBars": elapsed_time, "timeLoadFharmacies": elapsed_time2 }
        print("get_places data: ", json.dumps(results))
        return response
    except Exception as e:
        print(e)
        return None

@app.route('/locations/v1/api', methods=['GET'])
def home():
    return "El servidor esta inicializado en el puerto ????"

@app.route('/locations/v1/api/stores/near', methods=['GET'])
def storesNearby():
    latitud = request.args.get('latitud')
    longitud = request.args.get('longitud')
    rank_by = 'distance'
    if(latitud is None or longitud is None):
        return "You must to specify the latitud and longitud"

    # location = ('-34.8764965,-56.0947794')
    location = (latitud,longitud)
    distance = miles_to_meters(2500)
    return get_place_info(location, rank_by, distance)

@app.route('/locations/v1/api/bars/near', methods=['GET'])
def barsNearby():
    latitud = request.args.get('latitud')
    longitud = request.args.get('longitud')
    rank_by = 'distance'
    if(latitud is None or longitud is None):
        return "You must to specify the latitud and longitud"

    # location = ('-34.8764965,-56.0947794')
    location = (latitud,longitud)
    distance = miles_to_meters(6000)
    try:
        print("Start")
        # location = ('-34.8764965,-56.0947794')
        # get the start time
        st = time.time()
        bares = get_bares(location, rank_by, distance, None, True)
        # get the end time
        et = time.time()
        
        elapsed_time = et - st
        results = parse_data(bares)
        response = { "stores": results, "size": len(results), "timeLoadBars": elapsed_time }
        print("get_places data: ", json.dumps(results))
        return response
    except Exception as e:
        print(e)
        return None

@app.route('/locations/v1/api/footballfields/near', methods=['GET'])
def footballfieldsNearby():
    latitud = request.args.get('latitud')
    longitud = request.args.get('longitud')
    rank_by = 'distance'
    if(latitud is None or longitud is None):
        return "You must to specify the latitud and longitud"

    # location = ('-34.8764965,-56.0947794')
    location = (latitud,longitud)
    distance = miles_to_meters(6000)
    try:
        print("Start")
        # location = ('-34.8764965,-56.0947794')
        # get the start time
        st = time.time()
        bares = get_footballFields(location, rank_by, distance, None, True)
        # get the end time
        et = time.time()
        
        elapsed_time = et - st
        results = parse_data(bares)
        response = { "stores": results, "size": len(results), "timeLoadBars": elapsed_time }
        print("get_places data: ", json.dumps(results))
        return response
    except Exception as e:
        print(e)
        return None

@app.route('/locations/v1/api/pharmacies/near', methods=['GET'])
def pharmaciesNearby():
    latitud = request.args.get('latitud')
    longitud = request.args.get('longitud')
    rank_by = 'distance'
    if(latitud is None or longitud is None):
        return "You must to specify the latitud and longitud"

    # location = ('-34.8764965,-56.0947794')
    location = (latitud,longitud)
    distance = miles_to_meters(6000)
    try:
        print("Start")
        # location = ('-34.8764965,-56.0947794')
        # get the start time
        st = time.time()
        farmacias = get_pharmacies(location, rank_by, distance, None, True)
        # get the end time
        et = time.time()
        
        elapsed_time = et - st
        results = parse_data(farmacias)
        response = { "stores": results, "size": len(results), "timeLoadPharmacies": elapsed_time }
        print("get_places data: ", json.dumps(results))
        return response
    except Exception as e:
        print(e)
        return None

app.run()