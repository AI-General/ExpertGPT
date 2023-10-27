import requests

ENDPOINT = "http://localhost:5051"

def test_get_default_brains(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url=ENDPOINT+f'/brains/default/', headers=headers)
    print(f"status_code: {response.status_code}, \ttext: {response.text}")

if __name__ == '__main__':
    token = ""
    test_get_default_brains(token)