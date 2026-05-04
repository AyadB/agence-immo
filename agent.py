import anthropic
from outils import tools, chercher_biens

def run_agent(client, question, historique):
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