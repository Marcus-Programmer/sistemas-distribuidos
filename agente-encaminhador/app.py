from fastapi import FastAPI
from pydantic import BaseModel
import logging
from typing import Optional

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import spacy
from fastapi import FastAPI
from pydantic import BaseModel
import logging
from typing import Optional, List, Dict

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Carregamento do Modelo de IA (spaCy) ---
logger.info("[LOG] Iniciando o carregamento do modelo de IA do spaCy (pt_core_news_sm)...")
nlp = None
try:
    # Carrega o modelo de linguagem em português, otimizado para eficiência.
    nlp = spacy.load("pt_core_news_sm")
    logger.info("[LOG] Modelo do spaCy carregado com SUCESSO!")
except Exception as e:
    logger.error(f"[LOG] FALHA CRÍTICA ao carregar modelo do spaCy: {e}")
# ------------------------------------

app = FastAPI()

# Modelo de dados que o encaminhador espera receber do gateway
class Denuncia(BaseModel):
    texto: str
    classificacao: str
    confianca_modelo: Optional[float] = None

@app.post("/registrar-denuncia")
async def registrar_denuncia(denuncia: Denuncia):
    logger.info("--- AGENTE ENCAMINHADOR: INÍCIO DO PROCESSAMENTO ---")
    
    if not nlp:
        logger.error("[LOG] Tentativa de processamento mas o modelo spaCy não está disponível.")
        return {"erro": "Modelo de IA (spaCy) não está disponível."}

    texto_original = denuncia.texto
    logger.info(f"[LOG] ETAPA 1: Recebemos a denúncia classificada como '{denuncia.classificacao}'.")
    
    # Processa o texto com o modelo spaCy para encontrar entidades
    doc = nlp(texto_original)
    
    entidades_encontradas = []
    for entidade in doc.ents:
        # doc.ents contém as entidades nomeadas (NER) encontradas
        entidades_encontradas.append({
            "texto": entidade.text,
            "tipo": entidade.label_ # ex: 'PER' (Pessoa), 'LOC' (Local), 'ORG' (Organização)
        })
    
    logger.info(f"[LOG] ETAPA 2: Foram encontradas {len(entidades_encontradas)} entidades.")
    
    # Cria uma versão anonimizada do texto
    texto_anonimizado = texto_original
    for entidade in reversed(doc.ents): # Iterar de trás para frente para não bagunçar os índices
        texto_anonimizado = texto_anonimizado[:entidade.start_char] + f"[{entidade.label_}]" + texto_anonimizado[entidade.end_char:]

    logger.info("[LOG] ETAPA 3: Texto anonimizado com sucesso.")
    
    #
    # LÓGICA DE NEGÓCIO FUTURA:
    # Aqui você deve salvar o `texto_anonimizado` e as `entidades_encontradas`
    # em um banco de dados para análise futura, protegendo a privacidade.
    #
    
    logger.info("--- FIM DO PROCESSAMENTO ---")
    
    return {
        "status": "Denúncia processada e anonimizada com sucesso.",
        "texto_original": texto_original,
        "texto_anonimizado": texto_anonimizado,
        "entidades_identificadas": entidades_encontradas
    }


@app.get("/")
def health_check():
    # O healthcheck precisa ser rápido, não deve depender do modelo estar carregado.
    return {"status": "Agente encaminhador está online"}

app = FastAPI()

# Modelo de dados que o encaminhador espera receber do gateway
class Denuncia(BaseModel):
    texto: str
    classificacao: str
    confianca_modelo: Optional[float] = None


@app.post("/registrar-denuncia")
async def registrar_denuncia(denuncia: Denuncia):
    logger.info("--- DENÚNCIA RECEBIDA ---")
    logger.info(f"Classificação: {denuncia.classificacao}")
    logger.info(f"Confiança do Modelo: {denuncia.confianca_modelo:.4f}")
    logger.info(f"Texto: '{denuncia.texto[:80]}...'")
    
    #
    # LÓGICA DE NEGÓCIO FUTURA:
    # Aqui você poderia:
    # 1. Salvar a denúncia em um banco de dados (PostgreSQL, MongoDB).
    # 2. Enviar um e-mail de alerta para uma equipe de moderação.
    # 3. Integrar com um sistema de tickets (Jira, Zendesk).
    #
    
    logger.info("Denúncia registrada com sucesso (simulação).")
    logger.info("--- FIM DO REGISTRO ---")
    
    return {"status": "Denúncia registrada com sucesso."}


@app.get("/")
def health_check():
    return {"status": "Agente encaminhador está online"}
