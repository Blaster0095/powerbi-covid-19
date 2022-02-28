"""Publishing COVID-19 Vaccination dataset to PowerBI via REST API

This script allows the user to download the dataset for COVID-19 Vaccinations in the US from the CDC, formats the dataset appropriately using the create_dataset module, and publish it to PowerBI.

Dataset Link: https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-Jurisdi/unsk-b7fc

"""

from create_dataset import Row, Column, Table, Dataset, DatasetEncoder
from sodapy import Socrata
from datetime import datetime
import requests
import adal

date = datetime(2021, 1, 1)
date = date.strftime('%Y-%m-%d')

# Pulls COVID-19 vaccination dataset from CDC
client = Socrata("data.cdc.gov", None)

fields = ['date', 'location', 'distributed', 'distributed_janssen', 'distributed_moderna', 'distributed_pfizer', 'administered', 'administered_janssen', 'administered_moderna', 'administered_pfizer']
fields = ','.join(fields)
results = client.get("unsk-b7fc", select=fields, where=f"date > '{date}'")

# # Create rows
rows = []
for row in results:
    rows.append(Row(row))

# # Create columns
columns = []
columns.append(Column('date', 'datetime'))
columns.append(Column('location', 'string'))
columns.append(Column('distributed', 'Int64'))
columns.append(Column('distributed_janssen', 'Int64'))
columns.append(Column('distributed_moderna', 'Int64'))
columns.append(Column('distributed_pfizer', 'Int64'))
columns.append(Column('administered', 'Int64'))
columns.append(Column('administered_janssen', 'Int64'))
columns.append(Column('administered_moderna', 'Int64'))
columns.append(Column('administered_pfizer', 'Int64'))

# # Create table
tables = []
tables.append(Table(name='Vaccine_Distribution_Table', columns=columns, rows=rows))

# # Create dataset
dataset = Dataset(name='Vaccine_Distribution_Dataset', default_mode='Push', tables=tables)
datasetEncoder = DatasetEncoder()
encoded_dataset = datasetEncoder.encode(dataset)
print(encoded_dataset)

# Get authentication token
resource_url = 'https://analysis.windows.net/powerbi/api'
api_url = 'https://api.powerbi.com'
authority_url = 'https://login.windows.net/common'

api_version = 'v1.0'
api_org = 'org'

client_id = 'Azure_Client_Id'
client_secret = 'Azure_Client_Secret'

authentication_context = adal.AuthenticationContext(
    authority=authority_url,
    validate_authority=True,
    api_version=None
    )

token = authentication_context.acquire_token_with_client_credentials(
    resource=resource_url,
    client_id=client_id,
    client_secret=client_secret
    )

# Create post url
url = f'{api_url}/{api_version}/{api_org}/datasets'

# Push dataset to PowerBI
response = requests.post(url, headers={'Authorization': f'Bearer {token}'}, json=encoded_dataset)

