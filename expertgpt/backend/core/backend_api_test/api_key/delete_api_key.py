import requests

ENDPOINT = "http://localhost:5051"

def test_delete_api_key(token, key_id):
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    response = requests.delete(url=ENDPOINT+f'/api-key/{key_id}', headers=headers)
    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjZGY0MmNlNC1lZWIwLTQ5MWMtOWUwZS00MDRjNzg1ZDE1ZGEiLCJlbWFpbCI6InRlc3QzQGdtYWlsLmNvbSIsImV4cCI6MTY5ODgwOTk2M30.cmLl1xo0mssI9gZgxr-QzkZaVfBxPlx-GARfUqF2mTA'
    key_id = '831c5858-ee6b-4b72-b485-88613ba7a969'
    test_delete_api_key(token, key_id)
    