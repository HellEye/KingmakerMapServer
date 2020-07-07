import json

from flask import request

import db.Database as db
from KingmakerDB import app
from utils.parser import getDataAndColumns


@app.route("/api/settlement/improvements", methods=["GET"])
def getSettlementImprovements():
    outJson = json.dumps(db.get("settlement_improvements"))
    return outJson


@app.route("/api/settlement/improvements/<id>", methods=["GET"])
def getSettlementImprovementsBySettlementId(id=None):
    return json.dumps(db.get("settlement_improvements",
                             query=f"settlement.id='{id}'"))


@app.route("/api/settlement/improvements", methods=["PUT"])
def insertSettlementImprovement():
    data, columns = getDataAndColumns(request)
    outId=db.put("settlement_improvements", data, columns)
    return json.dumps({"id":outId})


@app.route("/api/settlement/improvements/<id>", methods=["DELETE"])
def deleteSettlementImprovement(id=None):
    db.delete('settlement_improvements', f"id='{id}'")
    return json.dumps([])
