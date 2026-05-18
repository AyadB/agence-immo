import streamlit as st
import sqlite3

def get_connection():
    return sqlite3.connect("data/agence.db")

def page_admin():
    st.title("🔧 Panel Admin — Bordeaux Immo")

    # Afficher tous les biens
    st.subheader("📋 Tous les biens")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, type, ville, quartier, prix, loyer, disponible FROM biens")
    biens = cursor.fetchall()
    conn.close()

    for bien in biens:
        id, type, ville, quartier, prix, loyer, disponible = bien
        statut = "✅ Disponible" if disponible else "❌ Non disponible"
        st.write(f"**{type} - {quartier}, {ville}** | Prix: {prix}€ | Loyer: {loyer}€ | {statut}")

    st.divider()

    # Ajouter un bien
    st.subheader("➕ Ajouter un bien")
    col1, col2 = st.columns(2)
    with col1:
        type_bien = st.selectbox("Type", ["Appartement", "Maison", "Studio"])
        ville = st.text_input("Ville")
        quartier = st.text_input("Quartier")
        surface = st.number_input("Surface (m²)", min_value=0)
        pieces = st.number_input("Pièces", min_value=1)
    with col2:
        prix = st.number_input("Prix d'achat (€)", min_value=0)
        loyer = st.number_input("Loyer mensuel (€)", min_value=0)
        description = st.text_area("Description")
        disponible = st.checkbox("Disponible", value=True)

    if st.button("Ajouter le bien"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO biens (type, ville, quartier, surface, pieces, prix, loyer, disponible, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            type_bien, ville, quartier, surface, pieces,
            prix if prix > 0 else None,
            loyer if loyer > 0 else None,
            1 if disponible else 0,
            description
        ))
        conn.commit()
        conn.close()
        st.success("Bien ajouté !")
        st.rerun()