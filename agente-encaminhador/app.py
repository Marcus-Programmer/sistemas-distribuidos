from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/encaminhar")
async def encaminhar(request: Request):
    body = await request.json()
    classificacao = body.get("classificacao")
    texto = body.get("texto")

    # Exemplo de lógica simples de resposta
    return {
        "status": "ok",
        "mensagem": f"Denúncia classificada como '{classificacao}' recebida e registrada.",
        "resumo": texto
    }
