import json

from flask import request, Blueprint

import db.Database as db

from utils.parser import getDataAndColumns

app=Blueprint('hex_improvements', 'KingmakerServer')

@app.route("/api/hexImprovements/<id>", methods=["GET"])
def getHexImprovement(id):
    out=db.get("hex_improvement", query=f"id={id}")
    if len(out)>0:
        out=out[0]
    else:
        return "null"
    return json.dumps({"id":out[0], "improvement":out[1], "hex":out[2]})

@app.route("/api/hexImprovements", methods=["PUT"])
def addHexImprovement():
    data, columns=getDataAndColumns(request)
    outId=db.put("hex_improvement", data, columns)
    return json.dumps({"id":outId, "name":"hexImprovements"})


@app.route("/api/hexImprovements/<id>", methods=["DELETE"])
def deleteBuildingDiscount(id=None):
    db.delete('hex_improvement', f"id={id}")
    return f'{{"id":{id}, "name":"hexImprovements"}}'