#Import modules
import asyncio, requests, json, datetime, random, pandas as pd, pyodbc
from azure.eventhub.aio import EventHubProducerClient
from dateutil.relativedelta import relativedelta
from azure.eventhub import EventData
from faker import Faker
fake = Faker('pt_BR')

server = 'tcp:srv-gasstation.database.windows.net' 
database = 'sql-gasstation' 
username = 'admingas' 
password = 'Zzoq5VbylQ2VaL93Hgbw'  
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
data = pd.read_sql("SELECT ISNULL(max(id),0) FROM customers", cnxn)

async def run():
    # Create a producer client to send messages to the event hub.
    producer = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://eh-gasstation.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=qcBczD3xI+dxDm2qQ1WKnYeCKMmvErFUqLfcxm2HCPQ=", eventhub_name="customer-topic")
    async with producer:
        customerid = int(data.iloc[0][0])
        # Add events to the batch.
        for x in range(100):
            # Create a batch.
            event_data_batch = await producer.create_batch()
            customerid = customerid + 1
            #generates custom data for each gender
            if fake.simple_profile()["sex"] == 'F':
                firstname = fake.first_name_female()
                sex = 'F'
                url = 'https://fakeface.rest/face/json?gender=female&minimum_age=999&maximum_age=999'
            else:
                firstname = fake.first_name_male()
                sex = 'M'
                url = 'https://fakeface.rest/face/json?gender=male&minimum_age=999&maximum_age=999'

            #custom a real name
            lastname = fake.last_name()
            middlename = fake.last_name()
            domainemail = fake.free_email_domain()
            username = firstname[0].lower().replace(' ', '') + lastname.lower().replace(' ', '')
            email = firstname.lower().replace(' ', '') + lastname.lower().replace(' ', '') + '@' + domainemail
            birthdate = fake.date_between(start_date='-90y', end_date='-10y')
            age = relativedelta(datetime.datetime.now(), birthdate)
            vehiclecategory = ["car", "motorcycle", "truck", "bus"]
            vehiclerandom = random.randint(0,len(vehiclecategory)-1)

            #find a picture based on age, using API Fake face and thispersondoesnotexist.
            url = url.replace('999', str(age.years))
            response = requests.get(url)
            if response.status_code == 200:
                imagelink = response.json()['image_url']
            else:
                imagelink = ""

            if age.years >= 16:
                job = fake.job()
            else:
                job = 'Estudante'
            #Create JSON
            Customer = {
                "id": customerid,
                "cpf": fake.cpf(),
                "originBranchId": random.randint(1,100),
                "name": firstname + ' ' + middlename + ' ' + lastname,
                "loginname": username,
                "password": fake.password(length=12),
                "email": email,
                "birthdate": birthdate.strftime('%Y-%m-%d'),
                "age": age.years,
                "job": fake.job(),
                "phone": fake.phone_number(),
                "gender": sex,
                "photo": imagelink,
                "cars": [
                    {
                    "type": vehiclecategory[vehiclerandom],
                    "plate": fake.license_plate()
                    }
                ],
                "addresses": [{
                    "addressStreet": fake.street_name(),
                    "addressNumber": fake.building_number(),
                    "addressCity": fake.city(),
                    "addressState": fake.state_abbr(),
                    "addressCountry": fake.current_country(),
                    "addressPostalCode": fake.postcode(),
                    "addressComplement": fake.neighborhood(),
                    "isMain": True
                }],
                "socialMidia": {
                    "facebook": "",
                    "instagram": "",
                    "linkeDin": "",
                    "twiter": ""
                },
                "createdDate": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                "lastRecentsOrders": [{
                    "orderNumber": "",
                    "orderTotal": ""
                }],
                "summary": {
                    "totalOrders": 0,
                    "totalVisits": 0,
                    "averageTicket": 0,
                    "lastOrderDate": 'null',
                    "lastFeedbackStatus": 'null',
                    "lastFeedbackMessage": 'null'
                },
                "possiblePromotions": [{
                    "productId": "",
                    "disacountPercent": 0
                }]
            }

            event_data_batch.add(EventData(json.dumps(Customer, indent=4)))
            #print(json.dumps(Customer, indent=4))
            print ("Event sent " + str(customerid) + " - time: " + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
            # Send the batch of events to the event hub.
            await producer.send_batch(event_data_batch)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
