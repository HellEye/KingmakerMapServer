import json

from flask import request, Blueprint

import db.Database as db
from utils.parser import getDataAndColumns

app = Blueprint('hex', 'KingmakerServer')
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
    rotation = 0

    def __init__(self, id, district, building, x, y, rotation):
        self.id = id
        self.district = district
        self.building = building
        self.x = x
        self.y = y
        self.rotation = rotation

    def toJson(self):
        return (
            f"""
            {{
                "id":{self.id},
                "district":{self.district},
                "building":{self.building},
                "x":{self.x},
                "y":{self.y},
                "rotation":{self.rotation}
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
        return out

    def toJson(self):
        return (
            f"""
            {{
                "id":{self.id},
                "buildings":{self.buildingToJson() if len(self.buildings) > 0 else "[]"}
            }}
            """
        )


class settlementImprovementDTO:
    id = 0
    settlement = 0
    building = 0

    def __init__(self, id, settlement, building):
        self.id = id
        self.settlement = settlement
        self.building = building

    def toJson(self):
        return f"""
        {{
            "id":{self.id},
            "settlement":{self.settlement},
            "building":{self.building}
        }}"""


class discountDTO:
    id = 0
    settlement = 0
    building = 0

    def __init__(self, id, settlement, building):
        self.id = id
        self.settlement = settlement
        self.building = building

    def toJson(self):
        return f"""
        {{
            "id":{self.id},
            "settlement":{self.settlement},
            "building":{self.building}
        }}"""


class settlementDTO:
    id = 0
    name = "Name"
    hexId = 0
    districts = []
    settlementImprovements = []

    def __init__(self, id, name, hexId, districts=None, settlementImprovements=None, discounts=None):
        if districts is None:
            districts = []
        if settlementImprovements is None:
            settlementImprovements = []
        if discounts is None:
            discounts = []
        self.id = id
        self.name = name
        self.hexId = hexId
        self.districts = districts
        self.settlementImprovements = settlementImprovements
        self.discounts = discounts

    def districtToJson(self):
        out = "["
        for d in self.districts:
            out += d.toJson() + ",\n"
        out = out[:-2]
        out += "]"
        return out

    def settlementImprovementsToJson(self):
        out = "["
        for s in self.settlementImprovements:
            out += s.toJson() + ",\n"
        out = out[:-2]
        out += "]"
        return out

    def discountsToJson(self):
        out = "["
        for s in self.discounts:
            out += s.toJson() + ",\n"
        out = out[:-2]
        out += "]"
        return out

    def toJson(self):
        return (
            f"""
            {{
                "id":{self.id},
                "name":"{self.name}",
                "hexId":{self.hexId},
                "districts":{self.districtToJson() if len(self.districts) > 0 else "[]"},
                "settlementImprovements":{self.settlementImprovementsToJson() if len(self.settlementImprovements) > 0 else "[]"},
                "discounts":{self.discountsToJson() if len(self.discounts) > 0 else "[]"}
            }}
            """
        )


class hexImprovementDTO:
    id = 0
    hex = 0
    improvement = 0

    def __init__(self, id, improvement, hex):
        self.id = id
        self.improvement = improvement
        self.hex = hex

    def toJson(self):
        return f"""
        {{
            "id":{self.id},
            "hex":{self.hex},
            "improvement":{self.improvement}
        }}
        """


class hexDataDTO:
    id = 0
    x = 0
    y = 0
    ownedBy = 0
    terrainType = 0
    settlement = None
    label=""

    def __init__(self, id, x, y, ownedBy, terrainType, label, settlement=None, hexImprovements=None):
        if hexImprovements is None:
            hexImprovements = []
        self.id = id
        self.x = x
        self.y = y
        self.ownedBy = ownedBy
        self.terrainType = terrainType
        self.settlement = settlement
        self.hexImprovements = hexImprovements
        self.label=label

    def getHexImprovements(self):
        out = "[\n"
        for i in self.hexImprovements:
            out += i.toJson() + ",\n"
        out = out[:-2]
        out += "]"
        return out

    def toJson(self):
        return (
            f"""{{
            "id":{self.id},
            "x":{self.x},
            "y":{self.y},
            "ownedBy": {self.ownedBy},
            "terrainType": {self.terrainType},
            "hexImprovements":{self.getHexImprovements() if len(self.hexImprovements) > 0 else "[]"},
            "settlement":{self.settlement.toJson() if self.settlement is not None else "{}"},
            "label":"{self.label if self.label is not None else ''}"
        }}"""
        )


@app.route("/api/hex", methods=["GET"])
def getHexes():
    outJson = json.dumps(db.get("hex"))
    return outJson


@app.route("/api/hex/<id>", methods=["GET"])
def getHexById(id=None):
    hex = db.get("hex", query=f"id={id}")
    if len(hex) > 0:
        hex = hex[0]
    else:
        return "null"
    return json.dumps({"id": hex[0], "xcoord": hex[1], "ycoord": hex[2], "ownedBy": hex[3], "terrainType": hex[4]})


@app.route("/api/hex", methods=["PUT"])
def insertHex():
    data, columns = getDataAndColumns(request)

    id = db.put("hex", data, columns)
    return json.dumps({"id": id, "name": "hex"})


@app.route("/api/hex/<x>-<y>", methods=["POST"])
def updateHex(x=None, y=None):
    data, columns = getDataAndColumns(request)
    hex = db.get("hex", query=f"xcoord={x} AND ycoord={y}")
    if len(hex) > 0:
        id = db.post("hex", data, columns, query=f"xcoord={x} AND ycoord={y}")
    else:
        id = db.put("hex", data, columns)
    return {"id": id, "name": "hex"}


@app.route("/api/hex/<x>-<y>", methods=["DELETE"])
def deleteHex(x=None, y=None):
    id=getHexByCoords(x, y)[0]
    db.delete('hex', query=f"xcoord={x} AND ycoord={y}")
    return f'{{"id":{id}, "name":"hex"}}'

@app.route("/api/hex/hexData", methods=["GET"])
def getFullHexData():
    hexes = db.get("hex")
    hexDTOs = []
    for hex in hexes:
        hexDTOs.append(hexDataDTO(hex[0], hex[1], hex[2], hex[3], hex[4], hex[5]))
    for hexDTO in hexDTOs:
        hexImprovements = db.get("hex_improvement", query=f"hex={hexDTO.id}")
        for impr in hexImprovements:
            hexDTO.hexImprovements.append(hexImprovementDTO(impr[0], impr[1], impr[2]))

        hexSettlement = db.get("settlement", query=f"hex={hexDTO.id}")
        if len(hexSettlement) > 0:
            hexDTO.settlement = settlementDTO(hexSettlement[0][0],
                                              hexSettlement[0][1],
                                              hexSettlement[0][2])

            settlementImprovements = db.get("settlement_improvements", query=f"settlement={hexDTO.settlement.id}")
            for s in settlementImprovements:
                improvement = settlementImprovementDTO(s[0], s[1], s[2])
                hexDTO.settlement.settlementImprovements.append(improvement)

            discounts = db.get("building_discount", query=f"settlement={hexDTO.settlement.id}")
            for d in discounts:
                discount = discountDTO(d[0], d[1], d[2])
                hexDTO.settlement.discounts.append(discount)

            districts = db.get("district", query=f"settlement={hexDTO.settlement.id}")
            for d in districts:
                district = districtDTO(d[0])
                hexDTO.settlement.districts.append(district)
                buildings = db.get("district_buildings", query=f"district={district.id}")
                for b in buildings:
                    district.buildings.append(buildingDTO(b[0], b[1], b[2], b[3], b[4], b[5]))

    out = "[\n"
    for dto in hexDTOs:
        out += dto.toJson() + ",\n"
    if len(out) > 3:
        out = out[:-2]
    out += "]"
    return out
