import spacy
import logging
from typing import Optional, List, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- Configuração do Logging ---
# Mantém apenas os logs mais importantes (INFO e acima)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Carregamento do Modelo de IA (spaCy) ---
logger.info("Carregando modelo de IA do spaCy (pt_core_news_sm)...")
nlp = None
try:
    # Carrega o modelo de linguagem em português
    nlp = spacy.load("pt_core_news_sm")
    logger.info("Modelo do spaCy carregado com sucesso!")
except Exception as e:
    logger.error(f"FALHA CRÍTICA ao carregar modelo do spaCy: {e}")
# ------------------------------------

app = FastAPI()

# Modelo de dados que o encaminhador espera receber do gateway
class Denuncia(BaseModel):
    texto: str
    classificacao: str
    confianca_modelo: Optional[float] = None

@app.post("/registrar-denuncia")
async def registrar_denuncia(denuncia: Denuncia):
    """
    Recebe uma denúncia, extrai entidades nomeadas e anonimiza o texto.
    """
    if not nlp:
        logger.error("Tentativa de processamento, mas o modelo spaCy não está disponível.")
        raise HTTPException(status_code=503, detail="Serviço de IA indisponível.")

    logger.info(f"Processando denúncia classificada como '{denuncia.classificacao}'.")
    texto_original = denuncia.texto
    
    # Processa o texto com o modelo spaCy para encontrar entidades
    doc = nlp(texto_original)
    
    entidades_encontradas = [
        {"texto": ent.text, "tipo": ent.label_} for ent in doc.ents
    ]
    
    # Cria uma versão anonimizada do texto
    texto_anonimizado = texto_original
    # Iterar de trás para frente para não bagunçar os índices de caracteres
    for entidade in reversed(doc.ents):
        texto_anonimizado = (
            texto_anonimizado[:entidade.start_char] + 
            f"[{entidade.label_}]" + 
            texto_anonimizado[entidade.end_char:]
        )

    logger.info(f"Denúncia processada. {len(entidades_encontradas)} entidades encontradas e anonimizadas.")
    
    # LÓGICA DE NEGÓCIO FUTURA:
    # Aqui você salvaria `texto_anonimizado` em um banco de dados.
    
    return {
        "status": "Denúncia processada e anonimizada com sucesso.",
        "texto_original": texto_original,
        "texto_anonimizado": texto_anonimizado,
        "entidades_identificadas": entidades_encontradas
    }

@app.get("/")
def health_check():
    """
    Endpoint de verificação de saúde para o Docker.
    """
    return {"status": "Agente encaminhador está online"}