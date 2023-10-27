import requests

ENDPOINT = "http://localhost:5051"

def test_get_public_prompts(token):
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    response = requests.get(url=ENDPOINT+f'/prompts', headers=headers)
    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    token = '123qweasd'
    test_get_public_prompts(token)
    