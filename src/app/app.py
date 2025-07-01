# Import packages
import os
import json
import duckdb
import logging
import datetime

from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Current time and date
current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Config logging
logging.basicConfig(

    level = logging.INFO,
    format = f'%(asctime)s - {current_time} - %(levelname)s - %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
)

# Load env variables
load_dotenv()

# API Key
API_KEY = os.getenv('FIRECRAWL_API_KEY')

# Check variables were loaded
if not API_KEY:
    logging.error('LOG - Erro: A variavel de ambiente FIRECRAWL_API_KEY nao foi definida')

    exit(1)

URL_TO_SCRAPE = "https://books.toscrape.com/"

# Database dir
DATABASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'database')
os.makedirs(DATABASE_DIR, exist_ok=True)
DUCKDB_FILE = os.path.join(DATABASE_DIR, "database.duckdb")

# Parametros de Processamento
PAGE_PROCESSING_OPTIONS = {

    # Extrair somente o conteudo da pagina princimal
    'onlyMainContent' : False
}

EXTRACTOR_OPTIONS = {}

OUTPUT_FORMAT = ['html']

# Funcao que orquestra o processo de scraping, armazemanto e analise

def scrape_store_analyze():
    """
    Orquestra o processo de scraping, armazenamento dos dados no DuckDB e análise dos resultados.
    1. Inicializa o FirecrawlApp com a API Key.
    2. Realiza scraping da URL alvo.
    3. Faz o parsing do HTML e extrai os dados dos livros (título e preço).
    4. Armazena os dados no banco DuckDB.
    5. Realiza análise simples (preço médio) usando SQL.
    """
    logging.info('LOG - Iniciando o processo de scraping, armazenamento e analise...')
    logging.info('LOG - Inicializando FirecrawlApp...')

    # Inicializa o FirecrawlApp
    try:
        app = FirecrawlApp(api_key=API_KEY)
    except Exception as e:
        logging.error(f"LOG - Falha ao iniciar o FirecrawlApp: {e}")
        return

    # Monta os parâmetros para o scraping
    scrape_params = {
        'formats': OUTPUT_FORMAT
    }
    if PAGE_PROCESSING_OPTIONS:
        scrape_params.update(PAGE_PROCESSING_OPTIONS)
    if EXTRACTOR_OPTIONS:
        logging.warning("LOG - Opcoes de Extractor definidas, mas nao usadas nessa versao do codigo")

    logging.info(f"LOG - Preparando para fazer o scraping na URL: {URL_TO_SCRAPE}")
    logging.info(f"LOG - Usando parametros: {json.dumps(scrape_params, indent=2)}")

    scraped_data = None
    html_content = None

    # Realiza o scraping da página
    try:
        logging.info(f"LOG - Scraping URL: {URL_TO_SCRAPE}...")
        scraped_data = app.scrape_url(URL_TO_SCRAPE, params=scrape_params)
        if scraped_data and 'html' in scraped_data and scraped_data['html']:
            html_content = scraped_data['html']
            logging.info("LOG - HTML obtido com sucesso.")
        else:
            logging.error("LOG - Falha ao obter HTML no scraping")
            return
    except Exception as e:
        logging.error(f"LOG - Ocorreu um erro durante o scraping: {e}", exc_info=False)
        return

    if html_content:
        logging.info("LOG - Iniciando o parsing do HTML e armazenamento no DuckDB...")
        try:
            # Faz o parsing do HTML
            soup = BeautifulSoup(html_content, 'lxml')
            product_pods = soup.select('article.product_pod')
            extracted_books = []
            logging.info(f"LOG - Encontrados {len(product_pods)} 'product_pods' para processar")
            # Extrai título e preço de cada livro
            for pod in product_pods:
                title_tag = pod.select_one('h3 a')
                title = title_tag['title'].strip() if title_tag and title_tag.has_attr('title') else None
                price_tag = pod.select_one('div.product_price p.price_color')
                price = None
                if price_tag:
                    price_text = price_tag.get_text()
                    try:
                        price_cleaned = price_text.replace('£', '').strip()
                        price = float(price_cleaned)
                    except ValueError:
                        logging.warning(f"LOG - Nao foi possivel converter o preco '{price_text}' para numero para o livro '{title}'.")
                if title and price is not None:
                    extracted_books.append({'title': title, 'price': price})
                else:
                    logging.warning(f"LOG - Dados incompletos para um livro. Titulo: {title}, Preco: {price}")
            if not extracted_books:
                logging.warning("LOG - Nenhum dado de livro valido extraido do HTML.")
                return
            logging.info(f"LOG - Extraidos {len(extracted_books)} livros com titulo e preco validos.")


            # Armazena os dados no DuckDB
            with duckdb.connect(database=DUCKDB_FILE, read_only=False) as con:
                logging.info(f"LOG - Conectado ao banco de dados DuckDB: {DUCKDB_FILE}")
                con.execute("""
                    CREATE TABLE IF NOT EXISTS books (
                        title VARCHAR,
                        price DECIMAL(10,2)
                    )
                """)
                logging.info("LOG - Tabela 'books' verificada/criada")
                con.execute("DELETE FROM books;")
                logging.info("LOG - Dados antigos da tabela 'books' removidos.")
                con.executemany(
                    "INSERT INTO books (title, price) VALUES (?, ?)",
                    [(book['title'], book['price']) for book in extracted_books]
                )
                logging.info(f"LOG - {len(extracted_books)} registros inseridos na tabela 'books'")
        except Exception as db_err:
            logging.error(f"LOG - Erro durante o parsing ou interacao com DuckDB: {db_err}", exc_info=True)
            return
        
        
        # Realiza análise dos dados
        logging.info("LOG - Iniciando a analise de preco medio via DuckDB")
        try:
            with duckdb.connect(database=DUCKDB_FILE, read_only=True) as con:
                result = con.execute("SELECT AVG(price) FROM books;").fetchone()
                book_count = con.execute("SELECT COUNT(*) FROM books;").fetchone()[0]
                if result and result[0] is not None:
                    average_price = result[0]
                    logging.info("LOG - Consulta SQL executada no DuckDB")
                    logging.info(f"LOG - Numero de livros na tabela para calculo: {book_count}")
                    logging.info(f"LOG - PRECO MEDIO (calculado pelo DuckDB): £{average_price:.2f}")
                else:
                    logging.info("LOG - Nao foi possivel calcular a media no DuckDB (tabela vazia ou erro na consulta)")
        except Exception as analysis_err:
            logging.info(f"LOG - Erro durante a analise no DuckDB: {analysis_err}", exc_info=True)
        logging.info("LOG - Analise concluida")
    else:
        logging.error("LOG - Conteudo HTML nao disponivel, analise cancelada...")

if __name__ == "__main__":
    scrape_store_analyze()
    logging.info("LOG - Processo finalizado.")
