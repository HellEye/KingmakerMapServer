import json

from flask import request

import db.Database as db
from KingmakerDB import app
from utils.parser import getDataAndColumns

"""
{
  "id": 0,
  "x": 0,
  "y": 0,
  "ownedBy": 0,
  "terrainType": 0,
  "settlement": {
    "id": 0,
    "name": "Name",
    "hexId": 0,
    "districts": [
      {
        "id": 0,
        "buildings": [
          0
        ]
      }
    ]
  }
}
"""


class buildingDTO:
    id = 0
    district = 0
    building = 0
    x = 0
    y = 0

    def __init__(self, id, district, building, x, y):
        self.id = id
        self.district = district
        self.building = building
        self.x = x
        self.y = y

    def toJson(self):
        return (
            f"""
            {{
                "id":{self.id},
                "district":{self.district},
                "building":{self.building},
                "x":{self.x},
                "y":{self.y}
            }}
            """
        )


class districtDTO:
    id = 0
    buildings = []

    def __init__(self, id, buildings=None):
        if buildings is None:
            buildings = []
        self.id = id
        self.buildings = buildings

    def buildingToJson(self):
        out = "["
        for b in self.buildings:
            out += b.toJson() + ","
        out = out[:-1]
        out += "]"

    def toJson(self):
        return (
            f"""
            {{
                "id":{self.id},
                "buildings":{self.buildingToJson() if len(self.buildings) > 0 else "[]"}
            }}
            """
        )


class settlementDTO:
    id = 0
    name = "Name"
    hexId = 0
    districts = []

    def __init__(self, id, name, hexId, districts=None):
        if districts is None:
            districts = []
        self.id = id
        self.name = name
        self.hexId = hexId
        self.districts = districts

    def districtToJson(self):
        out = "["
        for d in self.districts:
            out += d.toJson() + ","
        out = out[:-1]
        out += "]"
        return out

    def toJson(self):
        return (
            f"""
            {{
                "id":{self.id},
                "name":"{self.name}",
                "hexId":{self.hexId},
                "districts":{self.districtToJson() if len(self.districts) > 0 else "[]"}
            }}
            """
        )


class hexDataDTO:
    id = 0
    x = 0
    y = 0
    ownedBy = 0
    terrainType = 0
    settlement = None

    def __init__(self, id, x, y, ownedBy, terrainType, settlement=None):
        self.id = id
        self.x = x
        self.y = y
        self.ownedBy = ownedBy
        self.terrainType = terrainType
        self.settlement = settlement

    def toJson(self):
        return (
            f"""{{
            "id":{self.id},
            "x":{self.x},
            "y":{self.y},
            "ownedBy": {self.ownedBy},
            "terrainType": {self.terrainType},
            "settlement":{self.settlement.toJson() if self.settlement is not None else "{}"}
        }}"""
        )


@app.route("/api/hex", methods=["GET"])
def getHexes():
    outJson = json.dumps(db.get("hex"))
    return outJson


@app.route("/api/hex/<x>-<y>", methods=["GET"])
def getHexByCoords(x=None, y=None):
    return json.dumps(db.get("hex", query=f"xcoord={x} AND ycoord={y}"))


@app.route("/api/hex", methods=["PUT"])
def insertHex():
    data, columns = getDataAndColumns(request)

    db.put("hex", data, columns)
    return json.dumps([])


@app.route("/api/hex/<x>-<y>", methods=["POST"])
def updateHex(x=None, y=None):
    data, columns = getDataAndColumns(request)
    hex = db.get("hex", query=f"xcoord={x} AND ycoord={y}")
    if len(hex) > 0:
        print("Updating")
        db.post("hex", data, columns, query=f"xcoord={x} AND ycoord={y}")
    else:
        print("Creating new hex")
        db.put("hex", data, columns)
    return getHexByCoords(x, y)


@app.route("/api/hex/<x>-<y>", methods=["DELETE"])
def deleteHex(x=None, y=None):
    db.delete('hex', query=f"xcoord={x} AND ycoord={y}")
    return json.dumps([])


@app.route("/api/hex/hexData", methods=["GET"])
def getFullHexData():
    hexes = db.get("hex")
    hexDTOs = []

    for hex in hexes:
        hexDTOs.append(hexDataDTO(hex[0], hex[1], hex[2], hex[3], hex[4]))

    for hexDTO in hexDTOs:
        hexSettlement = db.get("settlement", query=f"hex={hexDTO.id}")
        if len(hexSettlement) > 0:
            hexDTO.settlement = settlementDTO(hexSettlement[0][0], hexSettlement[0][1], hexSettlement[0][2])
            districts = db.get("district", query=f"settlement={hexDTO.settlement.id}")
            for d in districts:
                district = districtDTO(d[0])
                hexDTO.settlement.districts.append(district)
                buildings = db.get("district_buildings", query=f"district={district.id}")
                for b in buildings:
                    district.buildings.append(buildingDTO(b[0], b[1], b[2], b[3], b[4]))

    out = "[\n"
    for dto in hexDTOs:
        out += dto.toJson() + ",\n"
    if len(out) > 3:
        out = out[:-2]
    out += "]"
    return out
