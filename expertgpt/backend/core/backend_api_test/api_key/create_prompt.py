import requests

ENDPOINT = "http://localhost:5051"

def test_create_prompt(token, create_prompt_properties):
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    response = requests.post(url=ENDPOINT+f'/signup', headers=headers, json=create_prompt_properties)
    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    token = '123qweasd'
    create_prompt_properties = {
        'title': 'pg test prompt',
        'content': 'This is pg test prompt',
        'status': 'private'
    }
    test_create_prompt(token, create_prompt_properties)
    