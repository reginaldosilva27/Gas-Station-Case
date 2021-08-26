#Import modules
import asyncio,datetime, random, json, pandas as pd, pyodbc
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from faker import Faker
fake = Faker('pt_BR')

server = 'tcp:srv-xxx.database.windows.net' 
database = 'sql-gasstation' 
username = 'admingas' 
password = 'xxx' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
data = pd.read_sql("select top 1000 p.id as productid, i.branchid,i.quantity,(select ISNULL(MAX(id),1) from providers) providerId from inventory i inner join products p on p.id = i.productid where i.quantity < 15000 order by NEWID()", cnxn)

#Preços dos produtos
#https://preco.anp.gov.br/
pricesGasoline = [2.0, 4.5]
pricesEthanol = [1.0, 3.5]
pricesDiesel = [2.0, 4.0]
pricesGas = [0.5, 3.0]
pricesOleo = [5, 20.0]

for index, x in data.iterrows():
    productrnd = random.randint(0,5)
    qtd = random.randrange(1000,30000 - x["quantity"],500)
    providerid = random.randrange(1, x["providerId"])
    priceswitch = {
        0: pricesGasoline,
        1: pricesGasoline,
        2: pricesEthanol,
        3: pricesDiesel,
        4: pricesGas,
        5: pricesOleo
    }
    price = priceswitch.get(productrnd)
    pricernd = round(random.uniform(price[0],price[1]),2) 
    Product = {
        "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
        "productId": x["productid"],
        "branchId": x["branchid"],
        "providerId": providerid,
        "entryDate": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        "unit": "LT",
        "quantity": qtd,
        "totalPrice": qtd * pricernd,
        "priceUnit": pricernd
        }
    print (Product)