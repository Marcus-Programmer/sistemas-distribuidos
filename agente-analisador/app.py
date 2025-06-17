from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/analise")
async def analisar_texto(request: Request):
    dados = await request.json()
    texto = dados.get("texto", "")

    if any(palavra in texto.lower() for palavra in ["ameaçou", "bateu", "violência", "machucou", "abuso", "medo"]):
        return {"classificacao": "abuso", "texto": texto}
    else:
        return {"classificacao": "normal", "texto": texto}
