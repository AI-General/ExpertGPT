import requests
from dotenv import load_dotenv

ENDPOINT = "http://localhost:5051"

def test_sign_up(email, password):
    params = {'email': email, 'password': password}
    response = requests.post(url=ENDPOINT+f'/signup', params=params)
    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    test_sign_up('robertdrivard89@gmail.com', 'pass')