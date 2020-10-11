from flask import Flask, make_response, Response, request
from flask_cors import CORS
from flask_socketio import SocketIO
import json
app = Flask("Kingmaker Server")
app.config['CORS_HEADERS'] = 'Content-Type'
socket = SocketIO(app, cors_allowed_origins="*")
CORS(app)
from rest.hex.Hex import app as blueprint_hex
from rest.hex.district import app as blueprint_district
from rest.hex.district_buildings import app as blueprint_districtBuildings
from rest.hex.building_discount import app as blueprint_buildingDiscounts
from rest.hex.hex_improvements import app as blueprint_hexImprovements
from rest.hex.settlement import app as blueprint_settlement
from rest.hex.settlement_improvements import app as blueprint_settlementImprovements
from rest.kingdoms.Kingdom import app as blueprint_kingdom
from rest.kingdoms.KingdomStats import app as blueprint_kingdomStats
from rest.hex.markers import app as blueprint_markers

# def sendEvent(name, data):
#     print(f'sending {name} with {data}')
#     socket.emit(name, data)
def notify(eventName):
    def notifyInner(func):
        def notifyWrapper(*args, **kwargs):
            out = func(*args, **kwargs)
            socket.emit(eventName, 'testValue')
            print(f"emitting {eventName} with {'testValue'}")
            return out

        notifyWrapper.__name__ = func.__name__
        return notifyWrapper

    return notifyInner


app.register_blueprint(blueprint_district)
app.register_blueprint(blueprint_districtBuildings)
app.register_blueprint(blueprint_buildingDiscounts)
app.register_blueprint(blueprint_hex)
app.register_blueprint(blueprint_hexImprovements)
app.register_blueprint(blueprint_kingdom)
app.register_blueprint(blueprint_kingdomStats)
app.register_blueprint(blueprint_settlement)
app.register_blueprint(blueprint_settlementImprovements)
app.register_blueprint(blueprint_markers)

@app.before_request
def beforeRequest():
    pass


@app.after_request
def afterRequest(body):
    response: Response = make_response(body)
    response.headers["Content-Type"] = "application/json"
    if request.method in ['PUT', 'POST', 'DELETE']:
        out=response.json
        print(f"emitting {out['name']} with {out['id']}")
        socket.emit(out['name'], out['id'])
    return response


@socket.on("test")
def onTestEvent(data):
    print(data)
    socket.emit("test2", 2)


if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=8255, debug=True)
    # app.run(host='0.0.0.0', port=8255, debug=True)
