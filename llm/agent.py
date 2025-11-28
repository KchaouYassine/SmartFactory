import sys
import json
import asyncio
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)     
sys.path.insert(0, project_root)            
sys.stdout.reconfigure(encoding="utf-8")


from get_groq_client import make_client
from client.kuba_shells import get_kuba_shells



async def get_kuba_informations() -> str:
    """
    Holt die aktuellen _KUBA-Shells über MCP und gibt sie als kompaktes JSON zurück.
    """
    kuba_shells = await get_kuba_shells()

    slim_shells = []
    for shell in kuba_shells:
        asset_info = shell.get("assetInformation", {}) or {}
        slim_shells.append(
            {
                "id": shell.get("id"),
                "idShort": shell.get("idShort"),
                # assetType sitzt in assetInformation
                "assetType":  shell.get("assetType") or asset_info.get("assetType"),
            }
        )

    return json.dumps(slim_shells, indent=2, ensure_ascii=False)


def get_kuba_answers(client, kuba_json: str, question: str) -> str:
    """
    Ruft das LLM bei Groq auf und beantwortet die Frage auf Basis des KUBA-JSONs.
    """
    system_prompt = (
        "You are an assistant for a SmartFactory holonic multi-agent system. "
        "You get JSON data about Asset Administration Shells (AAS) in the KUBA "
        "production island. Use ONLY this data to answer questions about KUBA "
        "holons and resources. If something is not in the data, say you don't know."
    )

    user_content = (
        f"User question:\n{question}\n\n"
        "Here is the current AAS data for namespace '_KUBA' as JSON:\n"
        f"{kuba_json}\n\n"
        "Answer the question in German, clearly and briefly."
    )

    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=0.2,
        top_p=0.5,
    )

    answer = chat_completion.choices[0].message.content.strip()
    return answer


# Direktes Test-Entry-Point: python -m llm.kuba_llm
if __name__ == "__main__":
    async def _test():
        # Frage definieren
        question = "Welche Shell-IDs gibt es in der KUBA-Produktionsinsel?"

        kuba_informations = await get_kuba_informations()

        client = make_client()

        answer = get_kuba_answers(client, kuba_informations, question=question)

        print("Antwort:\n", answer)

    asyncio.run(_test())
