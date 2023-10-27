import requests

ENDPOINT = "http://localhost:5051"

def test_get_api_keys(token):
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    response = requests.get(url=ENDPOINT+f'/api-keys', headers=headers)
    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    token = '123qweasd'
    test_get_api_keys(token)
    