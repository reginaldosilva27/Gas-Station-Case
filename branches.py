#Import modules
import asyncio, datetime, random, json, pandas as pd, pyodbc
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from faker import Faker
fake = Faker('pt_BR')

server = 'tcp:srv-gasstation.database.windows.net' 
database = 'sql-gasstation' 
username = 'admingas' 
password = 'Zzoq5VbylQ2VaL93Hgbw' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
data = pd.read_sql("SELECT ISNULL(max(id),0) FROM branches", cnxn)

async def run():
    # Create a producer client to send messages to the event hub.
    producerbranch = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://eh-gasstation.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=qcBczD3xI+dxDm2qQ1WKnYeCKMmvErFUqLfcxm2HCPQ=", eventhub_name="branches-topic")
    async with producerbranch:
      branchid = int(data.iloc[0][0])
      for x in range(100):
        event_data_batch = await producerbranch.create_batch()
        branchid = branchid + 1
        date = fake.date_between(start_date='-30y', end_date='today')
        Branch = {
          "id": branchid,
          "branchName": "Datainaction Gas Station - branch " + str(x), 
          "companyName": "Datainaction Gas Station LTDA",
          "cnpj": fake.cnpj(),
          "createdDate": date.strftime('%Y-%m-%dT%H:%M:%S'),
          "email": "branch" + str(x) + "@datainaction.dev",
          "phone": fake.phone_number(),
          "addressStreet": fake.street_name(),
          "addressNumber": fake.building_number(),
          "addressCity": fake.city(),
          "addressState": fake.state_abbr(),
          "addressCountry": fake.current_country(),
          "addressPostalCode": fake.postcode(),
          "addressComplement": fake.neighborhood()
        }
        print ("Event sent, branchId: " + str(branchid) + " - time: " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        event_data_batch.add(EventData(json.dumps(Branch, indent=4)))
        # Send the batch of events to the event hub.
        await producerbranch.send_batch(event_data_batch)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())