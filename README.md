# 🛡️ **Moderador Inteligente de Conteúdo com IA Distribuída**

## 🎯 O Problema (A "Dor")

A internet moderna é impulsionada por **conteúdo gerado por usuários (UGC)**. No entanto, o volume massivo de postagens diárias torna a **moderação manual**:

- Caríssima 💸  
- Psicologicamente desgastante 🧠💥  
- E operacionalmente insustentável ⚠️

Sem uma moderação eficaz, plataformas enfrentam:
- **Riscos legais**
- **Comprometimento da reputação**
- **Danos à saúde mental da comunidade**

> A solução? Um sistema **automatizado, inteligente e escalável**.

---

## 📊 Justificativa e Relevância

### 🚨 Crescimento de Discurso de Ódio

> 📈 Em 2022, denúncias no Brasil cresceram **67,7%** (SaferNet Brasil)

- 🧕‍ Intolerância religiosa: **+456%**
- 👩‍ Misoginia: **+251%**
- 🌍 Xenofobia: **+874%**

### 👶 Vulnerabilidade Infantojuvenil  
> 29% de crianças e adolescentes (9 a 17 anos) já enfrentaram **ofensas ou discriminação** online (TIC Kids Online Brasil 2024)

### 🧠 Fardo da Moderação Humana
> +50% dos moderadores relatam **sintomas de PTSD** devido à exposição a conteúdo extremo.

---

## 💡 Nossa Solução

Um sistema **distribuído** com três microserviços principais:

### 🛡️ API Gateway
> 🔗 Ponto central de entrada e orquestração entre os agentes.

### 🧠 Agente Analisador
> 💬 Realiza análise de sentimento com **IA/NLP**.  
> Classifica o texto como: `abuso` ou `normal`.

### 🕵️ Agente Encaminhador
> 🔒 Realiza **anonimização de dados sensíveis** usando NER (Reconhecimento de Entidades Nomeadas).

> **Objetivo:** Filtrar automaticamente o volume de conteúdo ofensivo e preservar a privacidade.

---

## 🧰 Tecnologias Utilizadas

| Categoria        | Ferramenta / Tecnologia                      |
|------------------|----------------------------------------------|
| 🐍 Linguagem      | Python 3.9                                   |
| ⚙️ API Framework | FastAPI                                      |
| 🧠 IA/NLP         | Transformers (Hugging Face), spaCy           |
| 📦 Containerização | Docker, Docker Compose                     |
| 🔁 Comunicação    | RESTful APIs (HTTP)                          |

---

## 🚀 Como Executar o Projeto

### 🔧 Pré-requisitos:
- Docker  
- Docker Compose  

### ⬇️ Clone o repositório:
```bash
git clone [URL-DO-SEU-REPOSITORIO]
cd [NOME-DA-PASTA]
```

### ⚙️ Construa e inicie os containers:
```bash
docker-compose build
docker-compose up
```

### 🧪 Teste o endpoint:
```bash
curl -X POST "http://localhost:8080/analisar-e-encaminhar" -H "Content-Type: application/json" -d '{"texto": "O João me ameaçou em Belo Horizonte."}'
```

---

## 📚 Referências

- 📖 [Agência Brasil (2023)](https://agenciabrasil.ebc.com.br/direitos-humanos/noticia/2023-02/denuncias-de-crimes-na-internet-com-discurso-de-odio-crescem-em-2022)  
- 📖 [Agência Brasil (2024)](https://agenciabrasil.ebc.com.br/geral/noticia/2024-10/tres-em-cada-dez-criancas-e-adolescentes-foram-ofendidos-na-internet)  
- 📖 [Fusion CX (2024)](https://www.fusioncx.com/blog/data-annotation/content-moderation/content-moderation-challenges/)

---

## 👥 Membros do Grupo

- Marcus Mendonça  
- Gustavo Muniz  
- Luiz Fernando  
- [Nome do Aluno 4 a ser preenchido]