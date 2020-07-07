import json

from flask import request

import db.Database as db
from KingmakerDB import app


# TODO add treasury and kingdom id
class KingdomStatsDTO:
    def __init__(self, array):
        self.id = array[0]
        self.alignment = array[1]
        self.economy = array[2]
        self.stability = array[3]
        self.loyalty = array[4]
        self.unrest = array[5]
        self.consumption = array[6]
        self.consumptionModifier = array[7]
        self.rulerAttributes = array[8]
        self.spymasterAttributes = array[9]
        self.ruler = array[10]
        self.consort = array[11]
        self.councilor = array[12]
        self.general = array[13]
        self.grandDiplomat = array[14]
        self.heir = array[15]
        self.highPriest = array[16]
        self.magister = array[17]
        self.marshal = array[18]
        self.royalEnforcer = array[19]
        self.spymaster = array[20]
        self.treasurer = array[21]
        self.viceroy = array[22]
        self.warden = array[23]
        self.treasury = array[24]
        self.kingdomId = array[25]
        self.controlDCMod = array[26]

    def toJson(self):
        return (
            f"""{{
            "alignment":{self.alignment},
            "economy":{self.economy},
            "stability":{self.stability},
            "loyalty":{self.loyalty},
            "unrest":{self.unrest},
            "consumption":{self.consumption},
            "consumptionModifier":{self.consumptionModifier},
            "treasury":{self.treasury},
            "positions":{{
                "ruler":{self.ruler},
                "rulerSelectedAttributes":{{
                    "stability":{"false" if self.rulerAttributes % 2 == 0 else "true"},
                    "loyalty":{"false" if self.rulerAttributes % 4 == 0 else "true"},
                    "economy":{"false" if self.rulerAttributes % 8 == 0 else "true"}
                }},
                "consort":{self.consort},
                "councilor":{self.councilor},
                "general":{self.general},
                "grandDiplomat":{self.grandDiplomat},
                "heir":{self.heir},
                "highPriest":{self.highPriest},
                "magister":{self.magister},
                "marshal":{self.marshal},
                "royalEnforcer":{self.royalEnforcer},
                "spymaster":{self.spymaster},
                "spymasterSelectedAttribute":{{
                    "stability":{"false" if self.spymasterAttributes != 1 else "true"},
                    "loyalty":{"false" if self.spymasterAttributes != 2 else "true"},
                    "economy":{"false" if self.spymasterAttributes != 3 else "true"}
                }},
                "treasurer":{self.treasurer},
                "viceroy":{self.viceroy},
                "warden":{self.warden}
                }},
            "kingdomId":{self.kingdomId},
            "controlDCMod":{self.controlDCMod}
            }}
            """
        )

    """
    INSERT INTO kingdom_stats (
    alignment,economy,stability,loyalty,unrest,consumption,consumption_modifier,
    rulerattributes,spymasterattributes,ruler,
    consort,councilor,general,granddiplomat,heir,highpriest,magister,marshal,
    royalenforcer,spymaster,treasurer,viceroy,warden,treasury,kingdomid) 
    VALUES (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

    """

    @staticmethod
    def getColumns():
        return ["alignment", "economy", "stability", "loyalty", "unrest", "consumption", "consumption_modifier",
                "rulerattributes", "spymasterattributes", "ruler",
                "consort", "councilor", "general", "granddiplomat", "heir", "highpriest", "magister", "marshal",
                "royalenforcer", "spymaster",
                "treasurer", "viceroy", "warden", "treasury", "kingdomId", "controldcmod"]

    def toArray(self):
        out = []
        out.append(self.alignment)
        out.append(self.economy)
        out.append(self.stability)
        out.append(self.loyalty)
        out.append(self.unrest)
        out.append(self.consumption)
        out.append(self.consumptionModifier)
        out.append(self.treasury)
        out.append(self.ruler)
        out.append(self.rulerAttributes)
        out.append(self.spymasterAttributes)
        out.append(self.consort)
        out.append(self.councilor)
        out.append(self.general)
        out.append(self.grandDiplomat)
        out.append(self.heir)
        out.append(self.highPriest)
        out.append(self.magister)
        out.append(self.marshal)
        out.append(self.royalEnforcer)
        out.append(self.spymaster)
        out.append(self.treasurer)
        out.append(self.viceroy)
        out.append(self.warden)
        out.append(self.kingdomId)
        out.append(self.controlDCMod)
        return out


def arrayFromFormData(form):
    out = []
    out.append(form["alignment"])
    out.append(form["economy"])
    out.append(form["stability"])
    out.append(form["loyalty"])
    out.append(form["unrest"])
    out.append(form["consumption"])
    out.append(form["consumptionModifier"])
    out.append(form["rulerAttributes"])
    out.append(form["spymasterAttributes"])
    out.append(form["ruler"])
    out.append(form["consort"])
    out.append(form["councilor"])
    out.append(form["general"])
    out.append(form["grandDiplomat"])
    out.append(form["heir"])
    out.append(form["highPriest"])
    out.append(form["magister"])
    out.append(form["marshal"])
    out.append(form["royalEnforcer"])
    out.append(form["spymaster"])
    out.append(form["treasurer"])
    out.append(form["viceroy"])
    out.append(form["warden"])
    out.append(form["treasury"])
    out.append(form["kingdomId"])
    out.append(form["controlDCMod"])
    return out


@app.route("/api/kingdomStats", methods=["GET"])
def getAllKingdomStats():
    row = db.get("kingdom_stats")
    if len(row) > 0 and len(row[0]) > 0:
        out = "["
        for kingdom in row:
            out += f"{KingdomStatsDTO(kingdom).toJson()},\n"
        if len(out) > 3:
            out = out[:-2]
        out += "]"
        return out
    else:
        return json.dumps([])


@app.route("/api/kingdomStats/<kingdomId>", methods=["GET"])
def getKingdomStats(kingdomId):
    row = db.get("kingdom_stats", query=f"kingdomId={kingdomId}")
    if len(row) > 0:
        return KingdomStatsDTO(row[0]).toJson()
    else:
        return json.dumps([])


@app.route("/api/kingdomStats/<kingdomId>", methods=["POST"])
def updateKingdomStats(kingdomId):
    data = arrayFromFormData(request.form)
    columns = KingdomStatsDTO.getColumns()
    db.post("kingdom_stats", data, columns, query=f"kingdomId={kingdomId}")
    return json.dumps([])


@app.route("/api/kingdomStats", methods=["PUT"])
def addKingdomStats():
    data = arrayFromFormData(request.form)
    columns = KingdomStatsDTO.getColumns()
    db.put("kingdom_stats", data, columns)
    return json.dumps([])
