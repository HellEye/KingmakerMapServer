import json

from flask import request, Blueprint
from flask_cors import cross_origin
import db.Database as db

from utils.parser import getDataAndColumns

app=Blueprint('kingdom', 'KingmakerServer')

@app.route("/api/kingdoms", methods=["GET"])
def getKingdoms():
    outJson = json.dumps(db.get("kingdoms"))
    return outJson


@app.route("/api/kingdoms/<id>", methods=["GET"])
def getKingdomById(id=None):
    out=db.get("kingdoms", query=f"id='{id}'")
    if len(out)>0:
        out=out[0]
    else:
        return "null"
    return json.dumps({"id":out[0], "name":out[1], "color":out[2]})


@app.route("/api/kingdoms", methods=["PUT"])
def insertKingdom():
    data, columns = getDataAndColumns(request)
    out=db.put("kingdoms", data, columns)
    return json.dumps({"id":out, "name": "kingdom"})


@app.route("/api/kingdoms/<id>", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def updateKingdom(id=None):
    data, columns = getDataAndColumns(request)
    db.post("kingdoms", data, columns, f"id='{id}'")
    return f'{{"id":{id}, "name":"kingdom"}}'

@app.route("/api/kingdoms/<id>", methods=["DELETE"])
def deleteKingdom(id=None):
    db.delete('kingdoms', f"id='{id}'")
    return f'{{"id":{id}, "name":"kingdom"}}'
