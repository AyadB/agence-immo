import os
os.environ["PYTHONIOENCODING"] = "utf-8"
import streamlit as st
import anthropic
from agent import run_agent
from auth import init_auth, verifier_login
from admin import page_admin

st.set_page_config(page_title="Bordeaux Immo", page_icon="🏠")

# Initialiser l'auth au démarrage
init_auth()

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# Initialiser la session
if "historique" not in st.session_state:
    st.session_state.historique = []
if "role" not in st.session_state:
    st.session_state.role = None

# Sidebar — login admin
with st.sidebar:
    if st.session_state.role == "admin":
        st.success("Connecté en tant qu'admin")
        if st.button("Se déconnecter"):
            st.session_state.role = None
            st.rerun()
    else:
        st.subheader("🔐 Connexion admin")
        username = st.text_input("Identifiant")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            role = verifier_login(username, password)
            if role:
                st.session_state.role = role
                st.rerun()
            else:
                st.error("Identifiants incorrects")

# Contenu principal
if st.session_state.role == "admin":
    page_admin()
else:
    st.title("🏠 Bordeaux Immo — Assistant")
    st.write("Bonjour ! Je suis votre assistant immobilier. Dites-moi ce que vous recherchez !")

    for msg in st.session_state.historique:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("Vous cherchez quoi ?")

    if question:
        st.session_state.historique.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("Je cherche..."):
                reponse = run_agent(client, question, st.session_state.historique)
                st.write(reponse)
                st.session_state.historique.append({"role": "assistant", "content": reponse})