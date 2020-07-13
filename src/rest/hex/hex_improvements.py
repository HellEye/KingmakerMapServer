import json

from flask import request

import db.Database as db
from KingmakerDB import app
from utils.parser import getDataAndColumns

@app.route("/api/hexImprovements", methods=["PUT"])
def addHexImprovement():
    data, columns=getDataAndColumns(request)
    outId=db.put("hex_improvement", data, columns)
    return json.dumps({"id":outId})


@app.route("/api/hexImprovements/<id>", methods=["DELETE"])
def deleteBuildingDiscount(id=None):
    db.delete('hex_improvement', f"id='{id}'")
    return json.dumps([])