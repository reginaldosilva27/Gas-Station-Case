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
data = pd.read_sql("select (select ISNULL(max(id),1000) from products),(select ISNULL(max(id),0) from providers)", cnxn)

async def run():
    # Create a producer client to send messages to the event hub.
    producerproduct = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://eh-gasstation.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=qcBczD3xI+dxDm2qQ1WKnYeCKMmvErFUqLfcxm2HCPQ=", eventhub_name="products-topic")
    producerprovider = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://eh-gasstation.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=qcBczD3xI+dxDm2qQ1WKnYeCKMmvErFUqLfcxm2HCPQ=", eventhub_name="provider-topic")
    async with producerprovider:
        async with producerproduct:
            productid = int(data.iloc[0][0])
            providerid = int(data.iloc[0][1])
            product = ["Gasolina","Gasolina Adt", "Etanol", "Diesel","Gas","Oleo"]
            date = fake.date_between(start_date='-30y', end_date='today')
            for x in range(10):
                event_data_batch_product = await producerproduct.create_batch()
                event_data_batch_provider = await producerprovider.create_batch()
                providerid = providerid + 1
                for y in range(6):
                    productid = productid + 1
                    Product = {
                        "id": productid,
                        "providerId": providerid,
                        "description": product[y],
                        "createdDate": date.strftime('%Y-%m-%dT%H:%M:%S'),
                        "enabled": True,
                        "unit": "LT",
                        "summary":{
                            "lastQuantity": 0,
                            "lastPrice": 0,
                            "laststockEntry": "null",
                            "lastOrderate":  "null",
                            "salesAmount": 0,
                            "totalSales": 0.00
                        }
                    }
                    print (">>>Product event sent " + str(Product["id"]) + " - time: " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
                    event_data_batch_product.add(EventData(json.dumps(Product, indent=4)))
                    await producerproduct.send_batch(event_data_batch_product)
            
                Provider = {
                    "id": providerid,
                    "originBranchId": random.randint(1,1000),
                    "companyName": fake.company(),
                    "cnpj": fake.cnpj(),
                    "createdDate": date.strftime('%Y-%m-%dT%H:%M:%S'),
                    "email": fake.email(),
                    "phone": fake.phone_number(),
                    "enabled": True,
                    "addresses": [{
                        "addressStreet": fake.street_name(),
                        "addressNumber": fake.building_number(),
                        "addressCity": fake.city(),
                        "addressState": fake.state_abbr(),
                        "addressCountry": fake.current_country(),
                        "addressPostalCode": fake.postcode(),
                        "addressComplement": fake.neighborhood(),
                        "isMain": True
                    }]
                }
                event_data_batch_provider.add(EventData(json.dumps(Provider, indent=4)))
                #print(json.dumps(Customer, indent=4))
                print ("Event sent " + str(providerid) + " - time: " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
                # Send the batch of events to the event hub.
                await producerprovider.send_batch(event_data_batch_provider)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())