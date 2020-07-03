from flask import Flask, make_response, Response, request
from flask_cors import CORS
import utils.parser
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.before_request
def beforeRequest():
    pass

@app.after_request
def afterRequest(body):
    response: Response = make_response(body)
    response.headers["Content-Type"]="application/json"
    return response


import rest.kingdoms.Kingdom
import rest.hex.Hex
import rest.kingdoms.KingdomStats
import rest.hex.settlement
import rest.hex.district
import rest.hex.district_buildings

