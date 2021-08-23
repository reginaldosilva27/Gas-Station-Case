# Gas-Station-Case

Nesse caso de uso iremos simular uma rede de postos de gasolina com milhares de filiais espalhados pelo Brasil, para suportar esse workload utilizaremos uma arquitetura de dados moderna e escalável com a Cloud da Microsoft.

O que veremos nessa lab:

- Gerar dados FAKE com Python
-   Os dados serão customizados para espelhar o mais próximo da realidade
- Ingestão dos dados gerados por filial (Dados no formato JSON)
-   Ingestão será toda feita pelo Azure Event Hubs
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

A rede de postos de Gasolina chamada "RCS Gas Station", possui cerca de 1000 filiais espalhadas pelo Brasil, as filiais operam com um sistema de redundância local, enviando dados via streaming em real-time para a central. A central recebe todos os dados como eventos e centraliza em seus repositórios.

Após os dados serem recebidos pela camada de ingestão, são processados de 3 formas diferentes:
- Enviados a uma camada RAW do Data Lake, sem nenhuma modificação.
- Tratados e enviados ao banco de dados Cosmos DB para consumo das APIs
- Tratados e enviados ao SQL Server (PaaS) para consumo do ERP

Os dados serão processados com Databricks e disponibilizado visões de negócio para visualização no Power BI e também consumo na API do Cosmos DB.

Iremos consumir 3 APIs para cruzamento de dados:
- Dados de clima
- Dados sobre dólar
- Dados sobre #RCAGASSTATION no Twiter
-   Aplicar análise de sentimento sobre as redes sociais

# Objetivo da arquitetura:

Prover uma solução escalável para momentos de picos, como promoções de combustível, possibilitar a geração de insights sobre dados semi-estruturados e estruturados em larga escala, cruzar dados externos de APIs e detectar anomalias em tempo real.

