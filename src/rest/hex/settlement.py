import json

from flask import request

import db.Database as db
from KingmakerDB import app
from utils.parser import getDataAndColumns


@app.route("/api/settlement", methods=["GET"])
def getSettlements():
    outJson = json.dumps(db.get("settlement"))
    return outJson


@app.route("/api/settlement/<id>", methods=["GET"])
def getSettlementById(id=None):
    return json.dumps(db.get("settlement",
                             query=f"id='{id}'"))



@app.route("/api/settlement", methods=["PUT"])
def insertSettlement():
    data, columns = getDataAndColumns(request)
    try:
        db.put("settlement", data, columns)
        return "200 OK"
    except e:
        return "500 ERROR"


@app.route("/api/settlement/<id>", methods=["POST"])
def updateSettlement(id=None):
    data, columns = getDataAndColumns(request)
    try:
        db.post("settlement", data, columns, f"id='{id}'")
        return "200 OK"
    except e:
        return "500 ERROR"


@app.route("/api/settlement/<id>", methods=["DELETE"])
def deleteSettlement(id=None):
    try:
        db.delete('settlement', f"id='{id}'")
        return "200 OK"
    except e:
        return "500 ERROR"