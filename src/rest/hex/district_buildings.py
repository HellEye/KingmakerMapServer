import json

from flask import request, Blueprint

import db.Database as db
from utils.parser import getDataAndColumns

app = Blueprint('districtBuildings', 'KingmakerServer')


@app.route("/api/district/buildings/<id>", methods=["GET"])
def getDistrictBuildings(id=None):
    out = db.get("district_buildings", query=f"id={id}")
    if len(out)>0:
        out=out[0]
    else:
        return "null"
    return json.dumps(
        {"id": out[0], "district": out[1], "building": out[2], "xcoord": out[3], "ycoord": out[4], "rotation": out[5]})


@app.route("/api/district/buildings", methods=["PUT"])
def insertDistrictBuilding():
    data, columns = getDataAndColumns(request)
    outId = db.put("district_buildings", data, columns)
    return json.dumps({"id": outId, "name":"districtBuildings"})


@app.route("/api/district/buildings/<id>/<xcoord>-<ycoord>", methods=["POST"])
def updateDistrictBuilding(id, xcoord, ycoord):
    data, columns = getDataAndColumns(request)
    outId = db.post("district_buildings", data, columns, f"xcoord={xcoord} AND ycoord={ycoord} AND district={id}")
    return f'{{"id": {id}, "name":"districtBuildings"}}'


@app.route("/api/district/buildings/<id>/<xcoord>-<ycoord>", methods=["DELETE"])
def deleteDistrictBuilding(id=None, xcoord=None, ycoord=None):
    db.delete('district_buildings', f"district='{id}' AND xcoord={xcoord} AND ycoord={ycoord}")
    return f'{{"id":{id}, "name":"districtBuildings"}}'
