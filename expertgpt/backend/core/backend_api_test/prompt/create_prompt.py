import requests

ENDPOINT = "http://localhost:5051"

def test_create_prompt(token, create_prompt_properties):
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    response = requests.post(url=ENDPOINT+f'/prompts', headers=headers, json=create_prompt_properties)
    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjOGRlYTU0Yy0wN2JlLTQ4ZjAtYTcwMS1iMGQ0OTliMGZiZmEiLCJlbWFpbCI6InRlc3QzQGdtYWlsLmNvbSIsImV4cCI6MTY5ODg1NTQ4OH0.555AXrAyoOsXq57Q9ofSeFV2fVTEI8ArXBR_rIPgP7M'
    create_prompt_properties = {
        'title': 'pg test prompt2',
        'content': 'This is pg test prompt content2',
        'status': 'private'
    }
    test_create_prompt(token, create_prompt_properties)
    