import requests

ENDPOINT = "http://localhost:5051"

def test_create_prompt(token, create_prompt_properties):
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    response = requests.post(url=ENDPOINT+f'/prompts', headers=headers, json=create_prompt_properties)
    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjZGY0MmNlNC1lZWIwLTQ5MWMtOWUwZS00MDRjNzg1ZDE1ZGEiLCJlbWFpbCI6InRlc3QzQGdtYWlsLmNvbSIsImV4cCI6MTY5ODgwOTk2M30.cmLl1xo0mssI9gZgxr-QzkZaVfBxPlx-GARfUqF2mTA'
    create_prompt_properties = {
        'title': 'pg test prompt2',
        'content': 'This is pg test prompt content2',
        'status': 'private'
    }
    test_create_prompt(token, create_prompt_properties)
    