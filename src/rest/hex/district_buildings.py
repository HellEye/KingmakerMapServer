import json

from flask import request

import db.Database as db
from KingmakerDB import app
from utils.parser import getDataAndColumns


@app.route("/api/district/buildings/<id>", methods=["GET"])
def getDistrictBuildings(id=None):
    return json.dumps(db.get("district RIGHT JOIN district_buildings ON district.id=district_buildings.district",
                             columns="district_buildings.xcoord, district_buildings.ycoord, district_buildings.building",
                             query=f"district.id='{id}'"))



@app.route("/api/district/buildings", methods=["PUT"])
def insertDistrictBuilding():
    data, columns = getDataAndColumns(request)
    try:
        db.put("district_buildings", data, columns)
        return "200 OK"
    except e:
        return "500 ERROR"


@app.route("/api/district/buildings/<id>/<xcoord>-<ycoord>", methods=["DELETE"])
def deleteDistrictBuilding(id=None, xcoord=None, ycoord=None):
    try:
        db.delete('district_buildings', f"district='{id}' AND xcoord={xcoord} AND ycoord={ycoord}")
        return "200 OK"
    except e:
        return "500 ERROR"
