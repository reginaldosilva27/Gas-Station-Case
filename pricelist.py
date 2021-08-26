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

pricelist = {
    "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
    "branchId": random.randint(1,100),
    "date": datetime.datetime.now().strftime('%Y-%m-%d'),
    "productId": 1,
    "productName": product[0],
    "unit": "LT",
    "price": round(random.uniform(priceswitch.get(0)[0],priceswitch.get(0)[1]),2)
    }
print (json.dumps(pricelist,indent=4))