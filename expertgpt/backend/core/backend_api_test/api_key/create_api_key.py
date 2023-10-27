import requests

ENDPOINT = "http://localhost:5051"

def test_create_api_key(token):
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    response = requests.post(url=ENDPOINT+f'/api-key', headers=headers)
    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    token = '123qweasd'
    test_create_api_key(token)
    