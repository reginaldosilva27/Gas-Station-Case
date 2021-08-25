#Import modules
from faker import Faker
fake = Faker('pt_BR')
import datetime, random
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey


HOST = 'https://xxxx.documents.azure.com:443/'
MASTER_KEY = 'xxxxx'
DATABASE_ID = 'gasstationdb'
CONTAINER_ID = 'products'

client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY} )
db = client.create_database_if_not_exists(id=DATABASE_ID)
container = db.create_container_if_not_exists(
    id=CONTAINER_ID, 
    partition_key=PartitionKey(path="/productId"),
    offer_throughput=400
)

product = ["Gasoline", "Ethanol", "Diesel","Natural gas","Lubricant"]
date = fake.date_between(start_date='-30y', end_date='today')
for x in range(1):
    x = x + 1
    Product = {
        "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
        "productId": x,
        "description": product[x-1],
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
        },
        "providers": [{
            "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
            "providerId": 1,
            "originBranchId": random.randint(1,100),
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
        },
        {
            "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
            "providerId": 2,
            "originBranchId": random.randint(1,100),
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
        },
        {
            "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
            "providerId": 3,
            "originBranchId": random.randint(1,100),
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
        ]
    }
    print(Product)
    print ("Event sent " + str(x) + " - time: " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))