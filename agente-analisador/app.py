from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Carregamento do Modelo de IA ---
logger.info("[LOG] Iniciando o carregamento do modelo de IA (isso pode demorar)...")
classificador_sentimento = None
try:
    # Usaremos um modelo mais leve (DistilBERT) para evitar problemas de memória.
    # Ele é mais rápido e consome menos RAM.
    classificador_sentimento = pipeline(
        "sentiment-analysis",
        model="lxyuan/distilbert-base-multilingual-cased-sentiments-student"
    )
    logger.info("[LOG] Modelo de IA carregado com SUCESSO!")
except Exception as e:
    logger.error(f"[LOG] FALHA CRÍTICA ao carregar modelo de IA: {e}")
# ------------------------------------

app = FastAPI()

class TextoParaAnalise(BaseModel):
    texto: str

@app.post("/analise")
async def analisar_texto(data: TextoParaAnalise):
    logger.info("--- INÍCIO DA ANÁLISE ---")
    
    if not classificador_sentimento:
        logger.error("[LOG] Tentativa de análise mas o modelo não está disponível.")
        return {"erro": "Modelo de IA não está disponível."}

    try:
        logger.info("[LOG] ETAPA 1: Recebemos o texto para análise.")
        texto_recebido = data.texto
        
        logger.info("[LOG] ETAPA 2: PREPARANDO PARA CHAMAR O MODELO DE IA.")
        resultado_analise = classificador_sentimento(texto_recebido)
        logger.info("[LOG] ETAPA 3: MODELO DE IA EXECUTADO COM SUCESSO.")

        primeiro_resultado = resultado_analise[0]
        label = primeiro_resultado['label']
        score = primeiro_resultado['score']
        logger.info(f"[LOG] ETAPA 4: Resultado do modelo: Label='{label}', Score={score:.4f}")

        # O modelo 'student' usa as labels 'positive', 'negative', 'neutral'.
        if label == "negative":
            classificacao = "abuso"
        else:
            classificacao = "normal"
        
        logger.info(f"[LOG] ETAPA 5: Classificação final: '{classificacao}'")
        
        resposta = {
            "classificacao": classificacao,
            "sentimento_detectado": label,
            "confianca_do_modelo": score
        }

        logger.info("[LOG] ETAPA 6: Preparando para enviar a resposta.")
        logger.info("--- FIM DA ANÁLISE ---")
        return resposta

    except Exception as e:
        logger.error(f"[LOG] ERRO INESPERADO DURANTE A ANÁLISE: {e}")
        return {"erro": "Uma falha ocorreu durante o processamento da análise."}


@app.get("/")
def health_check():
    return {"status": "Agente analisador (IA) está online"}
