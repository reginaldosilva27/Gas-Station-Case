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
data = pd.read_sql("select top 100 cpf,originBranchId, cartype,carplate from customers a where exists(select * from pricelist b where a.originBranchId = b.branchId)  order by NEWID()", cnxn)
pricestable = pd.read_sql("Select * from (select id,branchId,productId,productName,unit,price,date,ROW_NUMBER() over (Partition by branchId,productId order by date desc) as rnk from pricelist) tab where rnk = 1", cnxn)

async def run():
    # Create a producer client to send messages to the event hub.
    producersensor = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://eh-gasstation.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=qcBczD3xI+dxDm2qQ1WKnYeCKMmvErFUqLfcxm2HCPQ=", eventhub_name="sensors-topic")
    producerorder = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://eh-gasstation.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=qcBczD3xI+dxDm2qQ1WKnYeCKMmvErFUqLfcxm2HCPQ=", eventhub_name="orders-topic")
    async with producersensor:
        async with producerorder:
            #capacidade de litros por tipo de veiculo
            car = [5, 60]
            motorcycle = [1, 20]
            truck = [20, 200]
            bus = [20, 100]

            vehiclecapacity = {
                "car": car,
                "motorcycle": motorcycle,
                "truck": truck,
                "bus": bus
            }

            typefuel = {
                "car": ["Gasolina","Gasolina Adt","Etanol", "Gas"],
                "motorcycle": ["Gasolina","Gasolina Adt","Etanol"],
                "truck": ["Diesel"],
                "bus": ["Diesel"]
            }

            cardFlags = {
                0: "Mastercard",
                1: "Visa",
                2: "Elo",
                3: "Hipercard",
                4: "American Express"
            }

            paymentType = ["Credito", "Debito"]
            cont = 0
            for index, x in data.iterrows():
                event_data_batch_sensor = await producersensor.create_batch()
                event_data_batch_order = await producerorder.create_batch()
                cont = cont + 1
                capacityrnd = round(random.uniform(vehiclecapacity.get(x["cartype"])[0],vehiclecapacity.get(x["cartype"])[1]),2) 
                transactionId = fake.hexify(text='^^^^-^^^^-^^^^-^^^^')
                initialsensor = {
                    "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
                    "transactionId": transactionId,
                    "sensorId": 1,
                    "branchId": x["originBranchId"],
                    "dateLog": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                    "type": "in",
                    "cpf": x["cpf"],
                    "licensePlate": x["carplate"],
                    "vehicleCategory": x["cartype"],
                    "speedKm": random.randint(5,40)
                    }
                print (">>>Sensor 1 event sent " + str(initialsensor["transactionId"]) + " - time: " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
                event_data_batch_sensor.add(EventData(json.dumps(initialsensor, indent=4)))
                #await producersensor.send_batch(event_data_batch_sensor)

                timedelta = datetime.datetime.now() + datetime.timedelta(0,random.randint(5,30))
                stationid =  random.randint(2,8)
                stationsensorin = {
                    "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
                    "transactionId": transactionId,
                    "sensorId": stationid,
                    "branchId": x["originBranchId"],
                    "dateLog": timedelta.strftime('%Y-%m-%dT%H:%M:%S'),
                    "type": "in",
                    "cpf": x["cpf"],
                    "licensePlate": x["carplate"],
                    "vehicleCategory": x["cartype"],
                    "speedKm":0
                    }
                print (">>>Sensor 2 event sent " + str(stationsensorin["transactionId"]) + " - time: " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
                event_data_batch_sensor.add(EventData(json.dumps(stationsensorin, indent=4)))
                #await producersensor.send_batch(event_data_batch_sensor)

                timedelta = timedelta + datetime.timedelta(0,random.randint(120,600))
                rndFuel = random.randint(1,len(typefuel.get(x["cartype"])))
                fuel = typefuel.get(x["cartype"])[rndFuel-1]
                df = pricestable.loc[(pricestable["productName"] == fuel) & (pricestable["branchId"] == x["originBranchId"])]
            
                if len(df) > 0: 
                    payment = ""
                    rndflag = 0
                    card = ""
                    paymentTypernd = ""
                    installments = 1
                    cardNumber = ""
                    installmentsDate = datetime.datetime.now()
                    installmentsJson = [{
                        "installmentsId": "",
                        "installmentsNumber": 0,
                        "installmentsValue": 0.0,
                        "installmentsDate": installmentsDate.strftime('%Y-%m-%dT%H:%M:%S')
                        }]

                    if random.randint(1,2) == 1:
                        payment = "Cartao"
                        cardNumber = fake.credit_card_number()
                    else:
                        payment = "Dinheiro"

                    if payment == "Cartao":
                        rndflag = random.randint(0,4)
                        card = cardFlags.get(rndflag)
                        paymentTypernd = paymentType[random.randint(0,1)]

                    if paymentTypernd == "Credito":
                        if (round(capacityrnd * df.iloc[0]["price"],2)) > 100:
                            installments = random.randrange(0,12,2)
                            if installments == 0:
                                installments = 1
                        else:
                            installments = 1

                    if installments > 1:
                        for loop in range(installments):
                            installmentsDate = installmentsDate + datetime.timedelta(0,2592000)
                            installmentsJson.append({
                                "installmentsId": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
                                "installmentsNumber": loop+1,
                                "installmentsValue": round((capacityrnd * df.iloc[0]["price"]) / installments,2),
                                "installmentsDate": installmentsDate.strftime('%Y-%m-%dT%H:%M:%S')
                                })

                    if installments > 1:
                        installmentsJson.pop(0)

                    order = {
                        "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
                        "transactionId": transactionId,
                        "branchId": x["originBranchId"],
                        "dateLog": timedelta.strftime('%Y-%m-%dT%H:%M:%S'),
                        "cpf": x["cpf"],
                        "station": stationid,
                        "productId": int(df.iloc[0]["productId"]),
                        "quantity": capacityrnd,
                        "unit": "LT",
                        "priceUnit": df.iloc[0]["price"],
                        "totalPrice": round(capacityrnd * df.iloc[0]["price"],2),
                        "typePayment": payment,
                        "methodPayment": paymentTypernd,
                        "cardNumber": cardNumber,
                        "numberInstallments": installments,
                        "cardFlag": card,
                        "installments": installmentsJson,
                        }
                    print ("<<< Order event sent " + str(order["transactionId"]) + " - time: " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
                    event_data_batch_order.add(EventData(json.dumps(order, indent=4)))
                    await producerorder.send_batch(event_data_batch_order)
                    #print(json.dumps(order, indent=4))

                timedelta = timedelta + datetime.timedelta(0,random.randint(30,120))
                stationsensorout = {
                    "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
                    "transactionId": transactionId,
                    "sensorId": stationid,
                    "branchId": x["originBranchId"],
                    "dateLog": timedelta.strftime('%Y-%m-%dT%H:%M:%S'),
                    "type": "out",
                    "cpf": x["cpf"],
                    "licensePlate": x["carplate"],
                    "vehicleCategory": x["cartype"],
                    "speedKm": 0
                    }
                print (">>>Sensor 3 event sent " + str(stationsensorout["transactionId"]) + " - time: " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
                event_data_batch_sensor.add(EventData(json.dumps(stationsensorout, indent=4)))
                #await producersensor.send_batch(event_data_batch_sensor)

                timedelta = timedelta + datetime.timedelta(0,random.randint(30,120))
                exitsensor = {
                    "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
                    "transactionId": transactionId,
                    "sensorId": 10,
                    "branchId": x["originBranchId"],
                    "dateLog": timedelta.strftime('%Y-%m-%dT%H:%M:%S'),
                    "type": "out",
                    "cpf": x["cpf"],
                    "licensePlate": x["carplate"],
                    "vehicleCategory": x["cartype"],
                    "speedKm": random.randint(5,30)
                    }
                print (">>>Sensor 4 event sent " + str(exitsensor["transactionId"]) + " - time: " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
                event_data_batch_sensor.add(EventData(json.dumps(exitsensor, indent=4)))
                await producersensor.send_batch(event_data_batch_sensor)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())