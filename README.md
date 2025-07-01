# Webscraping Firecrawl + DuckDB + SQL Agent IA

## Visão Geral

Este projeto automatiza a extração, armazenamento e análise de dados de sites, integrando:
- **Firecrawl**: Webscraping automatizado.
- **DuckDB**: Banco de dados analítico local.
- **Agentes de IA (OpenAI + LangChain)**: Análise inteligente dos dados via linguagem natural.

Ideal para portfólio de Data Engineering, Data Science e automação de dados.

## Estrutura de Diretórios

```
webscreaping-duckdb-firecrawl/
│   README.md
│   requirements.txt
│
├───database/
│      database.duckdb
└───src/
    └───app/
        │   app.py
        │   app_ai_agent_analyzer.py
        │   .env_example
        │   .env
```

- O scraping e armazenamento estão em `src/app/app.py`.
- A análise com IA está em `src/app/app_ai_agent_analyzer.py`.
- O banco DuckDB é criado em `database/database.duckdb`.
- Variáveis de ambiente em `src/app/.env`.

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/marcelopachione/webscreaping-duckdb-firecrawl.git
   cd webscreaping-duckdb-firecrawl
   ```
2. **(Opcional) Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # ou
   source .venv/bin/activate  # Linux/Mac
   ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure as variáveis de ambiente:**
   - Copie `.env_example` para `.env` em `src/app/`.
   - Preencha `FIRECRAWL_API_KEY` (https://firecrawl.dev/pricing) e `OPENAI_API_KEY`.

## Como Executar

### 1. Scraping e Armazenamento
No diretório `src/app/`, execute:
```bash
python app.py
```
- Faz scraping da URL definida.
- Armazena os dados dos livros (título, preço) em `database/database.duckdb`.

### 2. Análise com Agente de IA
No mesmo diretório, execute:
```bash
python app_ai_agent_analyzer.py
```
- Realiza perguntas SQL inteligentes sobre os dados usando IA (OpenAI + LangChain).
- Exemplos de perguntas já inclusas no código.
- As respostas são salvas em `perguntas_respostas.txt`.

## Principais Dependências
- `firecrawl-py`, `duckdb`, `beautifulsoup4`, `python-dotenv`, `openai`, `langchain`, `langchain_community`, `langchain_openai`

Veja todas as dependências em `requirements.txt`.

## Observações
- O plano gratuito do Firecrawl possui limitações ([firecrawl.dev/pricing](https://firecrawl.dev/pricing)).
- Não compartilhe suas chaves de API publicamente.
- O diretório `database/` é criado automaticamente.
