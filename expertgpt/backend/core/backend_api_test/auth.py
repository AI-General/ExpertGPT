import requests
from dotenv import load_dotenv

ENDPOINT = "http://localhost:5051"

def test_sign_up(email, password):
    params = {'email': email, 'password': password}
    response = requests.post(url=ENDPOINT+f'/signup', params=params)
    print(response)

if __name__ == '__main__':
    test_sign_up('hongyuxiao05@gmail.com', 'password')