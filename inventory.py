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

product = ["Gasoline", "Ethanol", "Diesel","Natural gas","Lubricant"]
productrnd = random.randint(0,4)
qtd = random.randint(1000,20000)
price = round(random.random() * 5,2)
Product = {
    "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
    "productId": productrnd+1,
    "productName": product[productrnd],
    "branchId": random.randint(1,100),
    "providerId": random.randint(1,3),
    "entryDate": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
    "unit": "LT",
    "quantity": qtd,
    "totalPrice": qtd * price,
    "priceUnit": price
    }
print (Product)