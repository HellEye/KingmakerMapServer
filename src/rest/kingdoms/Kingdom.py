import json

from flask import request
from flask_cors import cross_origin
import db.Database as db
from KingmakerDB import app
from utils.parser import getDataAndColumns


@app.route("/api/kingdoms", methods=["GET"])
def getKingdoms():
    outJson = json.dumps(db.get("kingdoms"))
    return outJson


@app.route("/api/kingdoms/<id>", methods=["GET"])
def getKingdomById(id=None):
    return json.dumps(db.get("kingdoms", query=f"id='{id}'"))


@app.route("/api/kingdoms", methods=["PUT"])
def insertKingdom():
    data, columns = getDataAndColumns(request)
    db.put("kingdoms", data, columns)
    return json.dumps([])


@app.route("/api/kingdoms/<id>", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def updateKingdom(id=None):
    data, columns = getDataAndColumns(request)
    db.post("kingdoms", data, columns, f"id='{id}'")
    return json.dumps([])

@app.route("/api/kingdoms/<id>", methods=["DELETE"])
def deleteKingdom(id=None):
    db.delete('kingdoms', f"id='{id}'")
    return json.dumps([])
