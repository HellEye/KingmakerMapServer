import json

from flask import request, Blueprint

import db.Database as db

from utils.parser import getDataAndColumns

app=Blueprint('markers', 'KingmakerServer')

class MarkerDTO:
    def __init__(self, id, x, y, color):
        self.id=id
        self.x=x
        self.y=y
        self.color=color
    def toJson(self):
        return f"""
        {{
            "id":{self.id},
            "x":{self.x},
            "y":{self.y},
            "color":"{self.color}"
        }}
        """

def listToJson(list):
    if len(list)<=0:
        return "[]"
    out="[\n"
    for obj in list:
        out+=obj.toJson()+",\n"
    out=out[:-2]
    out+="]"
    return out

@app.route("/api/markers", methods=["GET"])
def getMarkers():
    outJson = db.get("markers")
    if len(outJson)<=0:
        return "[]"
    markerList=[]

    for marker in outJson:
        markerList.append(MarkerDTO(marker[0], marker[1], marker[2], marker[3]))
    return listToJson(markerList)

@app.route("/api/markers/<id>", methods=["GET"])
def getMarkerById(id):
    markerData=db.get("markers", query=f"id={id}")
    if len(markerData)<=0:
        return "null"
    markerData=markerData[0]
    return MarkerDTO(markerData[0], markerData[1], markerData[2], markerData[3]).toJson()

@app.route("/api/markers", methods=["PUT"])
def addMarker():
    data, columns = getDataAndColumns(request)
    outId=db.put("markers", data, columns)
    return f'{{"id":{outId}, "name":"markers"}}'

@app.route("/api/markers/<id>", methods=["DELETE"])
def deleteSettlement(id=None):
    db.delete('markers', f"id={id}")
    return f'{{"id":{id}, "name":"markers"}}'




