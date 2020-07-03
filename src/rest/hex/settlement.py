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
    print(data, columns)
    outId=db.put("settlement", data, columns)
    return json.dumps({"id":outId})


@app.route("/api/settlement/<id>", methods=["POST"])
def updateSettlement(id=None):
    data, columns = getDataAndColumns(request)
    db.post("settlement", data, columns, f"id='{id}'")
    return json.dumps([])


@app.route("/api/settlement/<id>", methods=["DELETE"])
def deleteSettlement(id=None):
    db.delete('settlement', f"id='{id}'")
    return json.dumps([])