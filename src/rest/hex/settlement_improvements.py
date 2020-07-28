import json

from flask import request, Blueprint

import db.Database as db
from utils.parser import getDataAndColumns

app = Blueprint('settlementImprovements', 'KingmakerServer')


@app.route("/api/settlement/improvements", methods=["GET"])
def getSettlementImprovements():
    outJson = json.dumps(db.get("settlement_improvements"))
    return outJson


@app.route("/api/settlement/improvements/<id>", methods=["GET"])
def getSettlementImprovementsById(id=None):
    out = db.get("settlement_improvements", query=f"id={id}")
    if len(out)>0:
        out=out[0]
    else:
        return "null"
    return json.dumps({"id": out[0], "settlement": out[1], "building": out[2]})


@app.route("/api/settlement/improvements", methods=["PUT"])
def insertSettlementImprovement():
    data, columns = getDataAndColumns(request)
    outId = db.put("settlement_improvements", data, columns)
    return f'{{"id": {outId}, "name": "settlementImprovements"}}'


@app.route("/api/settlement/improvements/<id>", methods=["DELETE"])
def deleteSettlementImprovement(id=None):
    db.delete('settlement_improvements', f"id={id}")
    return f'{{"id": {id}, "name": "settlementImprovements"}}'
