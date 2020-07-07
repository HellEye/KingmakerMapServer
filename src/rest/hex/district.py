import json

from flask import request

import db.Database as db
from KingmakerDB import app
from utils.parser import getDataAndColumns


@app.route("/api/district", methods=["GET"])
def getDistricts():
    outJson = json.dumps(db.get("district"))
    return outJson


@app.route("/api/district/<id>", methods=["GET"])
def getDistrictsBySettlementId(id=None):
    return json.dumps(db.get("district",
                             query=f"settlement='{id}'"))


@app.route("/api/district", methods=["PUT"])
def insertDistrict():
    data, columns = getDataAndColumns(request)
    outId=db.put("district", data, columns)
    return json.dumps({"id":outId})


@app.route("/api/district/<id>", methods=["POST"])
def updateDistrict(id=None):
    data, columns = getDataAndColumns(request)

    db.post("district", data, columns, f"id='{id}'")
    return json.dumps([])


@app.route("/api/district/<id>", methods=["DELETE"])
def deleteDistrict(id=None):
    db.delete('district', f"id='{id}'")
    return json.dumps([])
