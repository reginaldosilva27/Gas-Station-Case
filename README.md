# RCS Gas Station Case

Nesse caso de uso iremos simular uma rede de postos de gasolina com milhares de filiais espalhadas pelo Brasil, para suportar esse workload utilizaremos uma arquitetura de dados moderna e escalável com a Cloud da Microsoft.

O que veremos nesse projeto:

- Como gerar dados FAKE com Python
  - Os dados serão customizados para espelhar o mais próximo da realidade
- Ingestão dos dados gerados por filial (Dados no formato JSON)
  - Ingestão será toda feita pelo Azure Event Hubs
- Processar e extrair os dados streaming com o Azure Stream Analytics
- Armazenar os dados processados no Azure Cosmos DB para consumo das APIS
- Armazenar os dados processados no Azure SQL Database para consumo do ERP centralizado
- Armazenar os dados no Data lake, gravar no container Bronze no formato parquet
- Processar os dados com o Databricks, extrair dados da camada Bronze, aplicar limpeza dos dados e armazenar na camada Silver no formato delta
- Processar dados da camada Silver para camada Gold com as visões para consumo dos usuários finais
- Criar integração com Github
- Automatizar deploy com git actions

![image](https://user-images.githubusercontent.com/69867503/130528135-9ccc15b8-01f5-4ffa-ac58-0b3db046dc2b.png)

# Descrição do Case

A rede de postos de gasolina chamada "RCS Gas Station", possui mais de 1000 filiais espalhadas pelo Brasil, as filiais operam com um sistema de redundância local, enviando dados via streaming para a central. A central recebe os dados e armazena em seus repositórios.

Em média são gerados 100 eventos por minuto, porém, em casos de promoções a nível nacional, o fluxo de envio de dados poderá chegar a mais de 5 mil eventos por minuto.

A central precisa estar preparada para receber esses eventos e tomar decisões em tempo real sobre os dados gerados nas filiais.

Teremos 5 produtos principais e 3 fornecedores diferentes para cada produto.
- Gasolina
- Etanol
- Diesel
- Gás Natural
- Óleo Lubrificante

Cada posto terá 8 bombas ao total.

Os cadastros de clientes, produtos e fornecedores serão globais e únicos.

# Arquitetura

O objetivo do desenho acima é prover uma solução escalável para os momentos de pico, como promoções de combustível, possibilitar a geração de insights sobre dados semi-estruturados e estruturados em larga escala, cruzar dados externos de APIs e detectar anomalias em tempo real.

Dados gerados:
- Dados de sensores a cada minuto
  - Entrada e saída de novos veículos
  - Sensores de bombas
  - Sensores de temperatura e fumaça
- Dados dos pedidos de compra a cada minuto (Saída do estoque)
- Dados de recarga dos produtos a cada minuto (Entrada no estoque)
- Dados dos funcionários 1 vez ao dia (Excel)
- +2 novas filiais serão abertas todos os dias
- +1000 novos clientes por dia

Após os dados serem recebidos pela camada de ingestão, são processados de 3 formas diferentes:
- Enviados a uma camada RAW do Data Lake, sem nenhuma modificação.
- Tratados e enviados ao banco de dados Cosmos DB para consumo das APIs
- Tratados e enviados ao SQL Server (PaaS) para consumo do ERP

Os dados serão processados com Databricks e disponibilizado fatos e dimensões para visualização no Power BI e também devolvido métricas ao Cosmos DB para consumo das APIs.

Iremos consumir 3 APIs para cruzamento de dados:
- Dados de clima
- Dados sobre dólar
- Dados sobre #RCSGASSTATION no Twiter
  - Aplicar análise de sentimento sobre as redes sociais

# Tecnologias e linguagens utilizadas
- Azure Funcion
- Azure Event Hubs
- Azure Data Factory
- Azure Stream Analytics Jobs
- Azure Cosmos DB
- Azure SQL Database
- Azure Storage Account ADSL Gen2
- Azure Databricks
- Azure Synapse Serverless
- Azure Purview
- Power BI
- Excel
- APIs
- Python
- SQL

