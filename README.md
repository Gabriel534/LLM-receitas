## 🧠🍽️ LLM Recipe Recommender – DeepSeek-Prover-671B + LangChain + Food.com

Este projeto é uma aplicação de **customização de LLM (Large Language Model)** voltada para **recomendações inteligentes de receitas culinárias**, utilizando o modelo **[DeepSeek-Prover-671B](https://huggingface.co/DeepSeek-AI/deepseek-prover-671b)** via **HuggingFace**, com integração à biblioteca **LangChain** e dados extraídos do site **[Food.com](https://www.food.com/)**.

---

### 🔍 Objetivo

Permitir que usuários recebam **sugestões de receitas personalizadas** com base em:

* Preferências alimentares (ex: vegetariano, vegano, low carb)
* Restrições dietéticas (ex: sem lactose, sem glúten, alergias)
* Ingredientes disponíveis
* Ocasiões especiais (ex: jantar romântico, lanche escolar, refeição fitness)

---

### 🧩 Tecnologias Utilizadas

* 🧠 **LLM DeepSeek-Prover-671B** – via API HuggingFace
* 🔗 **LangChain** – para orquestração de prompts e manipulação de contexto
* 🍲 **Kaggle** – Coleta de dados do site Food.com
* 🧹 **Pré-processamento de dados** – limpeza, categorização e estruturação semântica
* 🗂️ **Custom Prompt Templates** – com foco em diálogo natural e adaptação à linguagem culinária

---

### ⚙️ Funcionalidades

* Entrada em linguagem natural (ex: "Quero uma receita sem carne com cogumelos e sem lactose")
* Geração de receitas ajustadas com substituições inteligentes
* Adaptação ao contexto do usuário (tipo de refeição, tempo disponível, nível de dificuldade)
* Modo de uso local com cache opcional de respostas
* API modular para integração em apps web ou bots

---

# 🚀 Como usar

# Instale as dependências
pip install -r requirements.txt

# Configure sua chave HuggingFace e rode o app
python main.py

---

### 📂 Estrutura do Projeto

├── main.py

└── README.md 

---

### 📋 Requisitos

* Python 3.10+
* Conta na HuggingFace com acesso ao modelo `deepseek-prover-671b`
* Chave API configurada via `.env`

### 📄 Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="sua_api_key_langsmith"
LANGSMITH_PROJECT="nome_do_projeto"
HUGGINGFACE_HUB_API_TOKEN="sua_api_token_huggingface"
```
---

### ✅ Próximas Etapas

* [ ] Avaliação automática da qualidade das respostas
* [ ] Interface gráfica
* [ ] Cache local das consultas frequentes
* [ ] Suporte a múltiplos idiomas

---

### 📘 Licença

Este projeto está licenciado sob a **MIT License**.

---
