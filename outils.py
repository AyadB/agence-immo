import sqlite3
import json

def get_connection():
    return sqlite3.connect("data/agence.db")

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
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM biens WHERE disponible = 1"
    params = []

    if ville:
        query += " AND LOWER(ville) LIKE ?"
        params.append(f"%{ville.lower()}%")
    if prix_max:
        query += " AND prix <= ?"
        params.append(prix_max)
    if loyer_max:
        query += " AND loyer <= ?"
        params.append(loyer_max)
    if pieces_min:
        query += " AND pieces >= ?"
        params.append(pieces_min)
    if type_bien:
        query += " AND LOWER(type) LIKE ?"
        params.append(f"%{type_bien.lower()}%")
    if surface_min:
        query += " AND surface >= ?"
        params.append(surface_min)

    cursor.execute(query, params)
    colonnes = [col[0] for col in cursor.description]
    resultats = [dict(zip(colonnes, ligne)) for ligne in cursor.fetchall()]
    conn.close()

    if not resultats:
        return "Aucun bien trouvé avec ces critères."
    return json.dumps(resultats, ensure_ascii=False)