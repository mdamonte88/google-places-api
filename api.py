from flask import Flask, request
from flask_cors import CORS
from app.routes import stores_nearby, bars_nearby, footballfields_nearby, pharmacies_nearby

app = Flask(__name__)
CORS(app, resources={r"/locations/v1/api/*": {"origins": ["https://www.gomarket.com.uy", "https://localdashboard.gomarket.com.uy", "https://local.gomarket.com.uy"]}})

app.config["DEBUG"] = False

API_KEY = open('API_KEY.txt').read()

@app.route('/locations/v1/api', methods=['GET'])
def home():
    return "El servidor está inicializado en el puerto ????"

@app.route('/locations/v1/api/health', methods=['GET'])
def health():
    return {
        "status": "ok",
        "message": "The server is healthy."
    }

@app.route('/locations/v1/api/stores/near', methods=['GET'])
def storesNearby():
    latitud = request.args.get('latitud')
    longitud = request.args.get('longitud')
    return stores_nearby(latitud, longitud)

@app.route('/locations/v1/api/bars/near', methods=['GET'])
def barsNearby():
    print('##### 1')
    latitud = request.args.get('latitud')
    longitud = request.args.get('longitud')
    return bars_nearby(latitud, longitud)

@app.route('/locations/v1/api/footballfields/near', methods=['GET'])
def footballfieldsNearby():
    latitud = request.args.get('latitud')
    longitud = request.args.get('longitud')
    return footballfields_nearby(latitud, longitud)

@app.route('/locations/v1/api/pharmacies/near', methods=['GET'])
def pharmaciesNearby():
    latitud = request.args.get('latitud')
    longitud = request.args.get('longitud')
    return pharmacies_nearby(latitud, longitud)

app.run()