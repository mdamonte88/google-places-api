import json
from flask import jsonify
import time
from utils import miles_to_meters, parse_data, get_stores

def get_footballFields(location, rankBy = None, distance = None, nextPage = None, isFirstTime = False):
    print("Get Football Fields \n\n\n")
    return get_stores(location, rankBy, distance, nextPage, isFirstTime, type = None, keyword="Futbol 5")

def get_bares(location, rankBy = None, distance = None, nextPage = None, isFirstTime = False):
    print("###3 Get Bars \n\n\n")
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


def stores_nearby(latitud, longitud):
    rank_by = 'distance'
    if latitud is None or longitud is None:
        return "You must specify the latitud and longitud"

    location = (latitud, longitud)
    distance = miles_to_meters(2500)
    return get_place_info(location, rank_by, distance)

def bars_nearby(latitud, longitud):
    print('##### 2')
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
        return jsonify({"error": "An error occurred"})
    
def footballfields_nearby(latitud, longitud):
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
    
def pharmacies_nearby(latitud, longitud):
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