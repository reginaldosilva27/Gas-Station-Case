#Import modules
import asyncio,datetime, random, json, pandas as pd, pyodbc
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from faker import Faker
fake = Faker('pt_BR')

server = 'tcp:srv-gasstation.database.windows.net' 
database = 'sql-gasstation' 
username = 'admingas' 
password = 'Zzoq5VbylQ2VaL93Hgbw' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
data = pd.read_sql("select top 1000 p.id as productid, p.description, i.branchid,i.quantity,(select ISNULL(MAX(id),1) from providers) providerId from inventory i inner join products p on p.id = i.productid where i.quantity < 15000 order by NEWID()", cnxn)

#Preços de compra dos produtos
#https://preco.anp.gov.br/
pricesGasoline = [2.0, 4.5]
pricesEthanol = [1.0, 3.5]
pricesDiesel = [2.0, 4.0]
pricesGas = [0.5, 3.0]
pricesOleo = [5, 20.0]

priceswitch = {
    "Gasolina": pricesGasoline,
    "Gasolina Adt": pricesGasoline,
    "Etanol": pricesEthanol,
    "Diesel": pricesDiesel,
    "Gas": pricesGas,
    "Oleo": pricesOleo
}

async def run():
    # Create a producer client to send messages to the event hub.
    producer = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://eh-gasstation.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=qcBczD3xI+dxDm2qQ1WKnYeCKMmvErFUqLfcxm2HCPQ=", eventhub_name="supplies-topic")
    async with producer:
        cont = 0
        for index, x in data.iterrows():
            event_data_batch = await producer.create_batch()
            #capacidade máxima de 30 mil litros
            qtd = random.randrange(1000,30000 - x["quantity"],500)
            providerid = random.randrange(1, x["providerId"])
            price = priceswitch.get(x["description"])
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
            #print (Product)
            event_data_batch.add(EventData(json.dumps(Product, indent=4)))
            print ("Event sent " + str(cont) + " - " + str(Product["id"]) + " - time: " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
            cont = cont + 1
            # Send the batch of events to the event hub.
            await producer.send_batch(event_data_batch)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())