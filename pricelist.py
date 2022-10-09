#Import modules
import asyncio,datetime, random, json, pandas as pd, pyodbc
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from faker import Faker
fake = Faker('pt_BR')

server = 'tcp:srv-xx.database.windows.net' 
database = 'sql-gasstation' 
username = 'admingas' 
password = 'xxxx' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
data = pd.read_sql("select a.id as productid,a.description, b.id as branchId from products a  cross join branches b order by b.id", cnxn)


#Preços de venda dos produtos com margem de lucro
pricesGasoline = [4.0, 8.0]
pricesEthanol = [3.0, 6.0]
pricesDiesel = [3.0, 7.0]
pricesGas = [2.0, 6.0]
pricesOleo = [15.0, 30.0]

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
    producer = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://eh-gasstation.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=xxxx", eventhub_name="pricelist-topic")
    async with producer:
        cont = 0
        for index, x in data.iterrows():
            # Create a batch.
            event_data_batch = await producer.create_batch()
            price = priceswitch.get(x["description"])
            pricernd = round(random.uniform(price[0],price[1]),2) 
            Pricelist = {
            "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
            "branchId": x["branchId"],
            "productId": x["productid"],
            "productName": x["description"],
            "unit": "LT",
            "price": pricernd,
            "date": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            }
            event_data_batch.add(EventData(json.dumps(Pricelist, indent=4)))
            print ("Event sent " + str(cont) + " - " + str(Pricelist["id"]) + " - time: " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
            cont = cont + 1
            # Send the batch of events to the event hub.
            await producer.send_batch(event_data_batch)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
