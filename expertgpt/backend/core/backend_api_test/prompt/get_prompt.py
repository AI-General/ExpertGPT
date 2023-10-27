import requests

ENDPOINT = "http://localhost:5051"

def test_get_prompt(token, prompt_id):
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    response = requests.get(url=ENDPOINT+f'/prompts/{prompt_id}', headers=headers)
    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    token = '123qweasd'
    prompt_id = ''
    test_get_prompt(token, prompt_id)
    