import json

from flask import request, Blueprint

import db.Database as db

from utils.parser import getDataAndColumns

app=Blueprint('improvements', 'KingmakerServer')

@app.route("/api/improvement", methods=["GET"])
def getImprovement():
    outJson = json.dumps(db.get("improvement"))
    return outJson


@app.route("/api/improvement/<name>", methods=["GET"])
def getImprovementByName(name=None):
    return json.dumps(db.get("improvement", query=f"name='{name}'"))

