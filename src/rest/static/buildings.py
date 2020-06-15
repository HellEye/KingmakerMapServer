import json

from flask import request

import db.Database as db
from KingmakerDB import app
from utils.parser import getDataAndColumns


@app.route("/api/building", methods=["GET"])
def getBuildings():
    outJson = json.dumps(db.get("buildings"))
    return outJson


@app.route("/api/building/<name>", methods=["GET"])
def getBuildingByName(name=None):
    return json.dumps(db.get("buildings", query=f"name='{name}'"))

