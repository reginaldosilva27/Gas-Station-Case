#Import modules
from faker import Faker
fake = Faker('pt_BR')
import datetime, random, json

#Preços dos produtos
product = ["Gasolina","Gasolina Adt", "Etanol", "Diesel","Gas","Oleo'"]

pricesGasoline = [4.0, 8.0]
pricesEthanol = [3.0, 6.0]
pricesDiesel = [3.0, 7.0]
pricesGas = [2.0, 6.0]
pricesOleo = [15.0, 30.0]

priceswitch = {
    0: pricesGasoline,
    1: pricesGasoline,
    2: pricesEthanol,
    3: pricesDiesel,
    4: pricesGas,
    5: pricesOleo
}

initialsensor = {
    "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
    "branchId": random.randint(1,100),
    "datetime": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
    "type": "in",
    "cpf": "",
    "licensePlate": "",
    "vehiclecategory": "",
    "speedKm": random.randint(5,50)
    }
print (json.dumps(initialsensor,indent=4))

stationsensorin = {
    "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
    "branchId": random.randint(1,100),
    "datetime": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
    "type": "in",
    "cpf": "",
    "licensePlate": "",
    "vehiclecategory": "",
    "station": 1
    }
print (json.dumps(stationsensorin,indent=4))

order = {
    "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
    "branchId": random.randint(1,100),
    "datetime": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
    "cpf": "",
    "station": 1,
    "productId": 1,
    "quantity": 20,
    "unit": "LT",
    "priceUnit": 3.45,
    "totalPrice": 69.0,
    "typePayment": "Dinheiro",
    "cardNumber": "",
    "installments": 0,
    "cardFlag": ""
    }
print (json.dumps(order,indent=4))

stationsensorout = {
    "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
    "branchId": random.randint(1,100),
    "datetime": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
    "type": "out",
    "cpf": "",
    "licensePlate": "",
    "vehiclecategory": "",
    "station": 1
    }
print (json.dumps(stationsensorout,indent=4))

exitsensor = {
    "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
    "branchId": random.randint(1,100),
    "datetime": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
    "type": "out",
    "cpf": "",
    "licensePlate": "",
    "vehiclecategory": "",
    "speedKm": random.randint(5,50)
    }
print (json.dumps(exitsensor,indent=4))