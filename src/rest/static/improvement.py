import json

from flask import request

import db.Database as db
from KingmakerDB import app
from utils.parser import getDataAndColumns


@app.route("/api/improvement", methods=["GET"])
def getImprovement():
    outJson = json.dumps(db.get("improvement"))
    return outJson


@app.route("/api/improvement/<name>", methods=["GET"])
def getImprovementByName(name=None):
    return json.dumps(db.get("improvement", query=f"name='{name}'"))

