import json

from flask import request

import db.Database as db
from KingmakerDB import app
from utils.parser import getDataAndColumns


@app.route("/api/settlement/discounts", methods=["GET"])
def getBuildingDiscounts():
    outJson = json.dumps(db.get("building_discounts"))
    return outJson


@app.route("/api/settlement/discounts/<id>", methods=["GET"])
def getBuildingDiscountsBySettlementId(id=None):
    return json.dumps(db.get("building_discounts",
                             query=f"settlement.id='{id}'"))


@app.route("/api/settlement/discounts", methods=["PUT"])
def insertBuildingDiscount():
    data, columns = getDataAndColumns(request)
    outId=db.put("building_discounts", data, columns)
    return json.dumps({"id":outId})


@app.route("/api/settlement/discounts/<id>", methods=["DELETE"])
def deleteBuildingDiscount(id=None):
    db.delete('building_discounts', f"id='{id}'")
    return json.dumps([])
