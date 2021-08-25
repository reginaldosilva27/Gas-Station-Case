#Import modules
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime
from faker import Faker
fake = Faker('pt_BR')

#declare variables
HOST = 'https://padariacasedb.documents.azure.com:443/'
MASTER_KEY = 'xxxxxxx'
DATABASE_ID = 'gasstationdb'
CONTAINER_ID = 'branches'

client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY} )
db = client.create_database_if_not_exists(id=DATABASE_ID)

container = db.create_container_if_not_exists(
    id=CONTAINER_ID, 
    partition_key=PartitionKey(path="/branchId"),
    offer_throughput=400
)

#loop to generate data and send to Cosmos DB
for x in range(100):
  x = x + 1
  date = fake.date_between(start_date='-30y', end_date='today')
  Branch = {
    "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
    "branchId": x,
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
  container.create_item(body=Branch)
  print ("Event sent, branchId: " + str(x) + " - time: " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
