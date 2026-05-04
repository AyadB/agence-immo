import sqlite3

conn = sqlite3.connect("data/agence.db")
cursor = conn.cursor()

# Tous les biens disponibles
print("=== Tous les biens ===")
cursor.execute("SELECT id, type, ville, prix, loyer FROM biens WHERE disponible = 1")
for ligne in cursor.fetchall():
    print(ligne)

# Juste les biens à Bordeaux
print("\n=== Biens à Bordeaux ===")
cursor.execute("SELECT type, quartier, prix FROM biens WHERE ville = 'Bordeaux'")
for ligne in cursor.fetchall():
    print(ligne)

# Biens sous 200 000€
print("\n=== Biens sous 200 000€ ===")
cursor.execute("SELECT type, ville, prix FROM biens WHERE prix <= 200000")
for ligne in cursor.fetchall():
    print(ligne)

conn.close()