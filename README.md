# Case - Datainaction Gas Station

Nesse projeto iremos simular uma rede de postos de combustíveis movida a dados, essa rede possui milhares de filiais espalhadas pelo Brasil, para suportar essa operação robusta utilizará uma arquitetura de dados moderna e escalável com a Cloud da Microsoft, vamos extrair o potencial dos dados e gerar visualizações e insights para esse negócio.

O que veremos nesse projeto:

- Como gerar dados FAKE com Python
  - Os dados serão customizados para espelhar o mais próximo da realidade
- Ingestão dos dados gerados por cada filial com o Event Hubs
- Processar e extrair os dados streaming com o Azure Stream Analytics
- Armazenar os dados processados no Azure Cosmos DB para consumo das APIS
- Armazenar os dados processados no Azure SQL Database para consumo do ERP centralizado
- Armazenar os dados no Data lake, armazenar em uma camada TRANSIENT ZONE com o formato original do dado
- Processar os dados com o Databricks, transformar os dados no formato PARQUET e copia-los para a camada RAW ZONE
- Processar os dados com o Databricks, extrair dados da camada RAW ZONE, aplicar limpeza dos dados e armazenar na camada TRUSTED ZONE no formato DELTA
- Processar dados da camada TRUSTED ZONE para a camada REFINED ZONE com as visões de negócio para consumo dos usuários finais
- Criar integração com Github
- Automatizar deploy com git actions
- Automatizar deploy dos recursos com TERRAFORM

![image](https://user-images.githubusercontent.com/69867503/130605392-6d817f53-baea-400c-96ce-f0a84fd915ca.png)
Referencia: https://www.datainaction.dev/

# Descrição do Case

A rede de postos de gasolina chamada "Datainaction Gas Station", possui mais de 1000 filiais espalhadas pelo Brasil, as filiais operam com um sistema local, enviando dados via streaming para a sede. A sede recebe os dados e armazena em seus repositórios centralizados na Cloud.

Em média são gerados 1000 eventos por minuto, porém, em casos de promoções a nível nacional, o fluxo de envio de dados poderá chegar a mais de 10 mil eventos por minuto.

A sede precisa estar preparada para receber esses eventos e tomar decisões em tempo real sobre os dados gerados nas filiais.

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

Essa arquitetura está focada em receber os dados 100% como streaming de eventos (Arquitetura Kappa proposta por Jay Kreps) centralizando a lógica de processamento em um único ponto.
![image](https://user-images.githubusercontent.com/69867503/130604361-feefe535-626e-4048-a176-5bbc37fac7ae.png)
Referencia: https://docs.microsoft.com/pt-br/azure/architecture/data-guide/big-data/

Também utilizares os conceitos da arquitetura Data Lakehouse, tirando proveito dos recursos e features disponibilizadas pela Databricks com o novo formato e engine de processamento Delta.
![image](https://user-images.githubusercontent.com/69867503/130604840-1104341f-5920-4782-b1e7-987339bf6036.png)
Referencia: https://databricks.com/blog/2020/01/30/what-is-a-data-lakehouse.html

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

Os dados serão processados com Databricks e disponibilizado no modelo de fatos e dimensões para visualização no Power BI e também devolvido métricas ao Cosmos DB para consumo das APIs.

Iremos consumir 3 APIs para cruzamento de dados:
- Dados de clima
- Dados sobre dólar
- Dados sobre #datainaction no Twiter
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

