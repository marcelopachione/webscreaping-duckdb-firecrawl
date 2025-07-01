# Webscraping Firecrawl + DuckDB + SQL Agent IA

## Descrição

Este projeto realiza automação de extração de dados da web utilizando o Firecrawl, armazena as informações coletadas no DuckDB para possibilitar análises em tempo real e emprega agentes de IA para gerar insights a partir dos dados obtidos. A solução integra tecnologias modernas para facilitar o processamento, análise e interpretação inteligente de grandes volumes de dados extraídos da web.

## Configuração da API Firecrawl

Para executar este projeto, é necessário criar uma conta no serviço Firecrawl e obter uma chave de API. Este projeto utiliza o plano gratuito ("Free Plan"), que possui algumas limitações. Para mais detalhes sobre as restrições, consulte o site: [firecrawl.dev/pricing](https://firecrawl.dev/pricing).

Após obter sua chave, adicione-a em um arquivo `.env` dentro da pasta `src/app` do projeto, seguindo o exemplo abaixo:

```
FIRECRAWL_API_KEY=sua_chave_aqui
```

Certifique-se de não compartilhar sua chave de API publicamente.

## Instalação de Dependências

Antes de executar o projeto, instale todos os pacotes necessários listados no arquivo `requirements.txt`. Para isso, utilize o comando abaixo no terminal:

```
pip install -r requirements.txt
```
