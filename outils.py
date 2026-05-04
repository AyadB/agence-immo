import json

with open("data/biens.json", "r", encoding="utf-8") as f:
    biens = json.load(f)

tools = [
    {
        "name": "chercher_biens",
        "description": "Cherche des biens immobiliers selon les critères du visiteur",
        "input_schema": {
            "type": "object",
            "properties": {
                "ville": {"type": "string", "description": "La ville recherchée"},
                "prix_max": {"type": "number", "description": "Budget maximum en euros"},
                "loyer_max": {"type": "number", "description": "Loyer maximum en euros"},
                "pieces_min": {"type": "number", "description": "Nombre de pièces minimum"},
                "type_bien": {"type": "string", "description": "Type de bien : Appartement, Maison, Studio"},
                "surface_min": {"type": "number", "description": "Surface minimum en m²"}
            }
        }
    }
]

def chercher_biens(ville=None, prix_max=None, loyer_max=None, pieces_min=None, type_bien=None, surface_min=None):
    resultats = [b for b in biens if b["disponible"]]
    if ville:
        resultats = [b for b in resultats if ville.lower() in b["ville"].lower()]
    if prix_max:
        resultats = [b for b in resultats if b["prix"] and b["prix"] <= prix_max]
    if loyer_max:
        resultats = [b for b in resultats if b["loyer"] and b["loyer"] <= loyer_max]
    if pieces_min:
        resultats = [b for b in resultats if b["pieces"] >= pieces_min]
    if type_bien:
        resultats = [b for b in resultats if type_bien.lower() in b["type"].lower()]
    if surface_min:
        resultats = [b for b in resultats if b["surface"] >= surface_min]
    if not resultats:
        return "Aucun bien trouvé avec ces critères."
    return json.dumps(resultats, ensure_ascii=False)