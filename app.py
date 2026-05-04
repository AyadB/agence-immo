import os
os.environ["PYTHONIOENCODING"] = "utf-8"
import streamlit as st
import anthropic
from agent import run_agent

st.set_page_config(page_title="Immo Assistant", page_icon="🏠")

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

st.title("🏠 Bordeaux Immo — Assistant")
st.write("Bonjour ! Je suis votre assistant immobilier. Dites-moi ce que vous recherchez !")

if "historique" not in st.session_state:
    st.session_state.historique = []

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