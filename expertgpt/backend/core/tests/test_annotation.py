import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logger
import requests
from dotenv import load_dotenv


load_dotenv()
logger = logger.get_logger(__name__)

ENDPOINT = "http://localhost:5051"

token = 'f214525d1bd6b3ad5b230b22f586dffd'
brain_id = '9ffb1e0e-84af-444e-a832-7db330baf06b'

headers = {'Authorization': f'Bearer {token}'}
# params = {'brain_id': brain_id}
data = {'text': 'Drinking cold water after meals can lead to cancer. This is because the cold water solidifies the oily substances that you have just consumed, which react with your stomach acid and produce toxins. These toxins subsequently lead to cancer.'}
response = requests.post(url=ENDPOINT+f'/annotation/{brain_id}', headers=headers, json=data)

print(response)
logger.info(f"status_code: {response.status_code}, \ttext: {response.text}")

