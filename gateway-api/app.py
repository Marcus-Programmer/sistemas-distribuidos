import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class TextoParaAnalise(BaseModel):
    texto: str

@app.post("/analisar-e-encaminhar")
async def analisar_e_encaminhar(data: TextoParaAnalise):
    texto_original = data.texto
    logger.info(f"Gateway recebeu texto para análise: '{texto_original[:50]}...'")

    try:
        # --- CORREÇÃO PRINCIPAL AQUI ---
        # A URL agora aponta para o endpoint /analise do serviço 'analisador'
        # O Docker resolve o nome 'analisador' para o IP correto na rede interna.
        url_analisador = "http://analisador:8000/analise"
        logger.info(f"Encaminhando para o Agente Analisador em: {url_analisador}")
        
        response_analisador = requests.post(url_analisador, json={"texto": texto_original})
        
        # Verifica se a requisição ao analisador foi bem sucedida (código 2xx)
        response_analisador.raise_for_status()
        
        resultado_analise = response_analisador.json()
        classificacao_ia = resultado_analise.get("classificacao")
        
        logger.info(f"Gateway recebeu a classificação: '{classificacao_ia}'")

        # Se a IA classificou como abuso, encaminha para o agente de denúncias
        if classificacao_ia == "abuso":
            logger.info("Classificado como 'abuso'. Encaminhando para o Agente Encaminhador.")
            url_encaminhador = "http://encaminhador:8001/registrar-denuncia"
            
            payload_denuncia = {
                "texto": texto_original,
                "classificacao": classificacao_ia,
                "confianca_modelo": resultado_analise.get("confianca_do_modelo")
            }
            
            response_encaminhador = requests.post(url_encaminhador, json=payload_denuncia)
            response_encaminhador.raise_for_status()
            
            return {"status": "Denúncia encaminhada com sucesso", "classificacao_ia": classificacao_ia}
        else:
            logger.info("Classificado como 'normal'. Nenhuma ação adicional.")
            return {"status": "Análise concluída, texto considerado normal.", "classificacao_ia": classificacao_ia}

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de comunicação entre serviços: {e}")
        raise HTTPException(status_code=503, detail=f"Erro de comunicação com um serviço interno: {e}")
    except Exception as e:
        logger.error(f"Ocorreu um erro inesperado no gateway: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado no gateway.")

@app.get("/")
def health_check():
    return {"status": "Gateway API está online"}
