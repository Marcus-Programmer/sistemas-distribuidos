# Use uma imagem base do Python
FROM python:3.9-slim

# Instala as ferramentas de build e o curl
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho
WORKDIR /app

# Copia o código da aplicação e a pasta do modelo local
COPY . .

# --- ETAPA DE DIAGNÓSTICO ---
# Lista todos os arquivos na pasta do modelo para verificar se foram copiados corretamente.
# Se esta etapa mostrar "No such file or directory" ou uma pasta vazia, o problema está na cópia.
RUN ls -lR /app/local_sentiment_model

# --- CORREÇÃO AQUI ---
# Aumentamos o timeout do pip para 600 segundos (10 minutos).
# Isso dá tempo de sobra para o pip baixar pacotes grandes como o 'torch'.
RUN pip install --no-cache-dir --timeout=600 -r requirements.txt

# Comando para iniciar o servidor da API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
