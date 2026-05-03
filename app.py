import os
os.environ["PYTHONIOENCODING"] = "utf-8"
import streamlit as st
import anthropic
import json

st.set_page_config(page_title="Immo Assistant", page_icon="🏠")

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

with open("biens.json", "r", encoding="utf-8") as f:
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
                "surface_min": {"typer": "number", "description": "Surface minimum en m²"}
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

def run_agent(question, historique):
    messages = []
    for msg in historique:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": question})
    
    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system="Tu es l'assistant de l'agence immobilière Bordeaux Immo. Tu aides les visiteurs à trouver des biens. Tu es chaleureux et professionnel. Tu réponds toujours en français. IMPORTANT : dès qu'un visiteur mentionne une ville ou un critère, utilise IMMÉDIATEMENT l'outil chercher_biens sans poser de questions. Montre les résultats d'abord, affine ensuite.",
            tools=tools,
            messages=messages
        )
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            break
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    resultats = chercher_biens(**block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": resultats
                    })
            messages.append({"role": "user", "content": tool_results})

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
            reponse = run_agent(question, st.session_state.historique)
            st.write(reponse)
            st.session_state.historique.append({"role": "assistant", "content": reponse})