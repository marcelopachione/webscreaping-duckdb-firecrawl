# Webscraping Firecrawl + DuckDB + SQL Agent IA

## Visão Geral

Este projeto automatiza a extração de dados de sites utilizando Firecrawl, armazena os dados em DuckDB e permite análises e geração de insights com agentes de IA. Ideal para portfólio de Data Engineering, Data Science e automação de dados.

## Estrutura de Diretórios

```
webscreaping-duckdb-firecrawl/
│   README.md
│   requirements.txt
│
└───src/
    ├───app/
    │   │   app.py
    │   │   .env_example
    │   │   .env
    └───database/
```

- O código principal está em `src/app/app.py`.
- O banco de dados DuckDB é criado em `src/database/database.duckdb`.
- As variáveis de ambiente são configuradas em `src/app/.env`.

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

   - Copie o arquivo `.env_example` para `.env` dentro de `src/app/`.
   - Preencha as chaves necessárias, especialmente `FIRECRAWL_API_KEY` (obtenha em https://firecrawl.dev) e, se for usar IA, `OPENAI_API_KEY`.

   Exemplo:
   ```env
   FIRECRAWL_API_KEY=sua_chave_aqui
   OPENAI_API_KEY=sua_chave_openai
   ```

## Como Executar

No diretório `src/app/`, execute:

```bash
python app.py
```

O script irá:
- Carregar as variáveis de ambiente.
- Validar a presença da chave da API Firecrawl.
- Realizar scraping da URL definida (`https://books.toscrape.com/`).
- Armazenar os dados coletados no banco DuckDB em `src/database/database.duckdb`.
- (Opcional) Utilizar agentes de IA para análise dos dados.

## Principais Dependências

- `firecrawl-py`: Cliente Python para Firecrawl
- `duckdb`: Banco de dados analítico
- `beautifulsoup4`: Parsing de HTML
- `python-dotenv`: Gerenciamento de variáveis de ambiente
- `openai`: Integração com agentes de IA (opcional)

Veja todas as dependências em `requirements.txt`.

## Observações

- O plano gratuito do Firecrawl possui limitações. Consulte [firecrawl.dev/pricing](https://firecrawl.dev/pricing).
- O diretório `src/database/` será criado automaticamente se não existir.