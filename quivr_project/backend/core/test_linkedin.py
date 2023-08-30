from selenium import webdriver
from linkedin_scraper import Person

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()
person = Person("https://www.linkedin.com/in/andre-iguodala-65b48ab5", driver=driver)
print(person)


# # pip install zenrows
# from zenrows import ZenRowsClient

# client = ZenRowsClient("3935a9723d4f528a9b218317734b60904cd7c593")
# url = "https://www.linkedin.com/in/andrewyng"
# params = {"js_render":"true","premium_proxy":"true"}

# response = client.get(url, params=params)

# print(response.text)


# pip install requests
import requests

url = 'https://www.linkedin.com/in/andrewyng'
apikey = '3935a9723d4f528a9b218317734b60904cd7c593'
params = {
    'url': url,
    'apikey': apikey,
	'js_render': 'true',
	'premium_proxy': 'true',
}
response = requests.get('https://api.zenrows.com/v1/', params=params)
print(response.text)


