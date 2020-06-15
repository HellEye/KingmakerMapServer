import json

from flask import request

import db.Database as db
from KingmakerDB import app
from utils.parser import getDataAndColumns


@app.route("/api/district", methods=["GET"])
def getDistricts():
    outJson = json.dumps(db.get("kingdoms"))
    return outJson


@app.route("/api/district/<id>", methods=["GET"])
def getDistrictsBySettlementId(id=None):
    return json.dumps(db.get("district LEFT JOIN settlement ON district.settlement=settlement.id",
                             columns="district.id, district.settlement",
                             query=f"settlement.id='{id}'"))



@app.route("/api/district", methods=["PUT"])
def insertDistrict():
    data, columns = getDataAndColumns(request)
    try:
        db.put("district", data, columns)
        return "200 OK"
    except e:
        return "500 ERROR"


@app.route("/api/district/<id>", methods=["POST"])
def updateDistrict(id=None):
    data, columns = getDataAndColumns(request)
    try:
        db.post("district", data, columns, f"id='{id}'")
        return "200 OK"
    except e:
        return "500 ERROR"


@app.route("/api/district/<id>", methods=["DELETE"])
def deleteDistrict(id=None):
    try:
        db.delete('district', f"name='{id}'")
        return "200 OK"
    except e:
        return "500 ERROR"
