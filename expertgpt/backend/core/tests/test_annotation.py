import os
import logger
import requests
from dotenv import load_dotenv


load_dotenv()
logger = logger.get_logger(__name__)

ENDPOINT = "http://localhost:5051"

token = 'f214525d1bd6b3ad5b230b22f586dffd'
brain_id = '9ffb1e0e-84af-444e-a832-7db330baf06b'

headers = {'Authorization': f'Bearer {token}'}
params = {'brain_id': brain_id}
response = requests.get(url=ENDPOINT+f'/annotation', headers=headers)

print(response)
logger.info(f"status_code: {response.status_code}, \ttext: {response.text}")

