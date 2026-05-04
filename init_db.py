import sqlite3
import json

# Connexion à la base de données (crée le fichier si il n'existe pas)
conn = sqlite3.connect("data/agence.db")
cursor = conn.cursor()

# Créer la table biens
cursor.execute("""
    CREATE TABLE IF NOT EXISTS biens (
        id INTEGER PRIMARY KEY,
        type TEXT,
        ville TEXT,
        quartier TEXT,
        surface REAL,
        pieces INTEGER,
        prix REAL,
        loyer REAL,
        disponible INTEGER,
        description TEXT
    )
""")

# Importer les données depuis le JSON existant
with open("data/biens.json", "r", encoding="utf-8") as f:
    biens = json.load(f)

for bien in biens:
    cursor.execute("""
        INSERT OR IGNORE INTO biens 
        (id, type, ville, quartier, surface, pieces, prix, loyer, disponible, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        bien["id"],
        bien["type"],
        bien["ville"],
        bien["quartier"],
        bien["surface"],
        bien["pieces"],
        bien["prix"],
        bien["loyer"],
        1 if bien["disponible"] else 0,
        bien["description"]
    ))

conn.commit()
conn.close()
print("Base de données créée avec succès !")