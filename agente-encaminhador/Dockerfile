# Use uma imagem base do Python
FROM python:3.9-slim

# --- CORREÇÃO AQUI ---
# Instala as ferramentas de build (como o compilador gcc) e o curl.
# O 'build-essential' é necessário para compilar dependências do spaCy, como a biblioteca 'blis'.
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo de dependências
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# --- ETAPA NOVA E IMPORTANTE ---
# Baixa o modelo de linguagem em português para o spaCy
RUN python -m spacy download pt_core_news_sm

# Copie o resto do código da aplicação
COPY . .

# Comando para iniciar o servidor da API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
