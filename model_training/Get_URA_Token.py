import requests
import model_training.Constants as Constants
import psycopg2

API_KEY = Constants.API_KEY

# URA API call (replace with the actual API URL and headers)
url = "https://www.ura.gov.sg/uraDataService/insertNewToken.action"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'AccessKey': API_KEY
}

response = requests.post(url,headers=headers)
data = response.json()
token = data['Result']

url = "https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=4"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'AccessKey': API_KEY,
    'Token': token
}

response = requests.get(url, headers=headers)
data = response.json()

count = 0
for i in data['Result']:
    for transaction in i['transaction']:
        count += 1

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="ura_data", user="postgres", password="password123", host="localhost"
)
cursor = conn.cursor()

# Parse the JSON response and insert it into the database
trans_count = 0

for project in data['Result']:
    project_name = project['project']
    market_segment = project['marketSegment']
    try:
        latitude = float(project['y'])
        longitude = float(project['x'])
    except KeyError:
        latitude = longitude = 0
    street = project['street']

    # Iterate over each transaction
    for transaction in project['transaction']:
        property_type = transaction['propertyType']
        if property_type != 'Executive Condominium':
            continue
        
        trans_count += 1
        print(f"Inserting transaction, total count: {trans_count}")
        contract_date = transaction['contractDate']
        area = float(transaction['area'])
        price = float(transaction['price'])
        type_of_area = transaction['typeOfArea']
        tenure = transaction['tenure']
        floor_range = transaction['floorRange']
        type_of_sale = transaction['typeOfSale']
        district = transaction['district']
        no_of_units = int(transaction['noOfUnits'])

        # Insert into the property_transactions table
        cursor.execute("""
            INSERT INTO property_transactions (
                project_name, market_segment, contract_date, area, price, property_type, 
                type_of_area, tenure, floor_range, type_of_sale, district, street, 
                latitude, longitude, no_of_units
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            project_name, market_segment, contract_date, area, price, property_type,
            type_of_area, tenure, floor_range, type_of_sale, district, street,
            latitude, longitude, no_of_units
        ))

# Commit the transaction and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully.")