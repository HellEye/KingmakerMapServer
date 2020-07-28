import json

from flask import request

import db.Database as db
from utils.parser import getDataAndColumns
from flask import Blueprint

app=Blueprint('buildingDiscounts', 'KingmakerServer')

@app.route("/api/settlement/discounts", methods=["GET"])
def getBuildingDiscounts():
    outJson = json.dumps(db.get("building_discount"))
    return outJson


@app.route("/api/settlement/discounts/<id>", methods=["GET"])
def getBuildingDiscountById(id=None):
    out=db.get("building_discount", query=f"id='{id}'")
    if len(out)>0:
        out=out[0]
    else:
        return "null"
    print(f'{{"id":{out[0]}, "settlement":{out[1]}, "building":{out[2]}}}')
    return f'{{"id":{out[0]}, "settlement":{out[1]}, "building":{out[2]}}}'


@app.route("/api/settlement/discounts", methods=["PUT"])
def insertBuildingDiscount():
    data, columns = getDataAndColumns(request)
    print("TEST")
    outId=db.put("building_discount", data, columns)
    print(f'{{"id":{outId}, "name":"buildingDiscount"}}')
    return f'{{"id":{outId}, "name":"buildingDiscount"}}'


@app.route("/api/settlement/discounts/<id>", methods=["DELETE"])
def deleteBuildingDiscount(id=None):
    db.delete('building_discount', f"id='{id}'")
    return f'{{"id":{id}, "name":"buildingDiscount"}}'
