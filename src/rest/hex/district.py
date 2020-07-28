import json

from flask import request, Blueprint

import db.Database as db

from utils.parser import getDataAndColumns

app=Blueprint('district', 'KingmakerServer')
@app.route("/api/district", methods=["GET"])
def getDistricts():
    outJson = json.dumps(db.get("district"))
    return outJson


@app.route("/api/district/<id>", methods=["GET"])
def getDistrictsById(id=None):
    out=db.get("district", query=f"id='{id}'")
    if len(out)>0:
        out=out[0]
    else:
        return "null"
    return json.dumps({"id":id, "settlement":out[1]})


@app.route("/api/district", methods=["PUT"])
def insertDistrict():
    data, columns = getDataAndColumns(request)
    outId=db.put("district", data, columns)
    return json.dumps({"id":outId, "name":"district"})


@app.route("/api/district/<id>", methods=["POST"])
def updateDistrict(id=None):
    data, columns = getDataAndColumns(request)

    db.post("district", data, columns, f"id='{id}'")
    return f'{{"id":{id}, "name":"district"}}'


@app.route("/api/district/<id>", methods=["DELETE"])
def deleteDistrict(id=None):
    db.delete('district', f"id='{id}'")
    return f'{{"id":{id}, "name":district}}'
