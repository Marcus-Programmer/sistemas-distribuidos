from fastapi import FastAPI, Request
import requests

app = FastAPI()  # <-- ISSO DEVE VIR ANTES

@app.post("/analisar-e-encaminhar")
async def analisar_e_encaminhar(request: Request):
    dados = await request.json()

    resposta_analisador = requests.post("http://analisador:8000/analise", json=dados)
    resultado = resposta_analisador.json()

    if resultado.get("classificacao") == "abuso":
        requests.post("http://encaminhador:8001/encaminhar", json=resultado)

    return {"status": "ok", "resultado": resultado}
