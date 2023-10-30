import requests

ENDPOINT = "http://localhost:5051"

def test_create_prompt(token, prompt_id, prompt_update_properties):
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    response = requests.put(url=ENDPOINT+f'/prompts/{prompt_id}', headers=headers, json=prompt_update_properties)
    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjZGY0MmNlNC1lZWIwLTQ5MWMtOWUwZS00MDRjNzg1ZDE1ZGEiLCJlbWFpbCI6InRlc3QzQGdtYWlsLmNvbSIsImV4cCI6MTY5ODgwOTk2M30.cmLl1xo0mssI9gZgxr-QzkZaVfBxPlx-GARfUqF2mTA'
    prompt_id = 'd4394a1a-08a5-4d30-921b-3926d35313a3'
    prompt_update_properties = {
        # 'title': 'pg test prompt',
        'content': 'This is updated pg test prompt2',
        'status': 'public'
    }
    test_create_prompt(token, prompt_id, prompt_update_properties)
    