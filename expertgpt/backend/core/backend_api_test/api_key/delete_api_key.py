import requests

ENDPOINT = "http://localhost:5051"

def test_delete_api_key(token, key_id):
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    response = requests.delete(url=ENDPOINT+f'/api-key/{key_id}', headers=headers)
    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    token = '123qweasd'
    key_id = ''
    test_delete_api_key(token, key_id)
    