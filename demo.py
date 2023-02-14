from pprint import pprint
import os
import googlemaps #pip install googlemaps

API_KEY = open('API_KEY.txt').read()
map_client = googlemaps.Client(API_KEY)

def miles_to_meters(miles):
    try:
        print('Meters', miles * 1.609,344)
        return miles * 1.609,344
    except:
        return 0

def get_place_info():
    try: 
        location = ('-34.8764965,-56.0947794')
        distance = miles_to_meters(500)
        response = map_client.places_nearby(
            type='restaurant|pharmacy',
            location=location,
            radius = distance
        )
        results = response.get('results')
        print("Termine")
        return results
    except Exception as e:
        print(e)
        return None

print("Start Demo py")
place_info = get_place_info()
for i in range(0, len(place_info)):
    company = place_info[i]
    print('*****************************')
    print('Place_id:', company['place_id'])
    print('Nombre del local:', company['name'])
    if ('business_status' in company):
        print('Busines Status :', company['business_status'])
    if ('opening_hours' in company): 
        print('Abre :', company['opening_hours'])
    if ('location' in company):
        print('Location :', company['location'])
    if ('rating' in company):
        print('Rating :', company['rating'])
    print('Vicinity', company['vicinity'])

    # print('Place_id:', company['place_id'])
    # print('Address:', company['formatted_address'])
    # print('Geometry:', company['geometry'])
    # print('Rating:', company['rating'])

