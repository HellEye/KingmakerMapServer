import json

from flask import request, Blueprint

import db.Database as db

from utils.parser import getDataAndColumns

app=Blueprint('settlement', 'KingmakerServer')

@app.route("/api/settlement", methods=["GET"])
def getSettlements():
    outJson = json.dumps(db.get("settlement"))
    return outJson


@app.route("/api/settlement/<id>", methods=["GET"])
def getSettlementById(id=None):
    out=db.get("settlement", query=f"id={id}")
    if len(out)>0:
        out=out[0]
    else:
        return "null"
    return json.dumps({"id":out[0], "name":out[1], "hex":out[2]})


@app.route("/api/settlement", methods=["PUT"])
def insertSettlement():
    data, columns = getDataAndColumns(request)
    print(data, columns)
    outId=db.put("settlement", data, columns)
    return json.dumps({"id":outId, "name":"settlements"})


@app.route("/api/settlement/<id>", methods=["POST"])
def updateSettlement(id=None):
    data, columns = getDataAndColumns(request)
    db.post("settlement", data, columns, f"id='{id}'")
    return f'{{"id":{id}, "name":"settlements"}}'


@app.route("/api/settlement/<id>", methods=["DELETE"])
def deleteSettlement(id=None):
    db.delete('settlement', f"id={id}")
    return f'{{"id":{id}, "name":"settlements"}}'