import requests

ENDPOINT = "http://localhost:5051"

def test_create_prompt(token, prompt_id, prompt_update_properties):
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    response = requests.put(url=ENDPOINT+f'/prompts/{prompt_id}', headers=headers, json=prompt_update_properties)
    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    token = '123qweasd'
    prompt_id = ''
    prompt_update_properties = {
        'title': 'pg test prompt',
        'content': 'This is pg test prompt',
        'status': 'private'
    }
    test_create_prompt(token, prompt_id, prompt_update_properties)
    