import sqlite3
import bcrypt

def get_connection():
    return sqlite3.connect("data/agence.db")

def init_auth():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT
        )
    """)
    # Créer un admin par défaut
    mot_de_passe = "admin123"
    hash = bcrypt.hashpw(mot_de_passe.encode(), bcrypt.gensalt()).decode()
    cursor.execute("""
        INSERT OR IGNORE INTO utilisateurs (username, password_hash, role)
        VALUES (?, ?, ?)
    """, ("admin", hash, "admin"))
    conn.commit()
    conn.close()

def verifier_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash, role FROM utilisateurs WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if not result:
        return None
    hash_stocke, role = result
    if bcrypt.checkpw(password.encode(), hash_stocke.encode()):
        return role
    return None