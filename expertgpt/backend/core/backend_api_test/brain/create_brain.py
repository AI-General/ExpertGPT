import requests

ENDPOINT = "http://localhost:5051"

def test_create_brain(token, create_brain_data):
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    response = requests.post(ENDPOINT + '/brains/', json=create_brain_data, headers=headers)
    print(f"status_code: {response.status_code}, \ttext: {response.text}")


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmOWQyZTg0Yi00NDRmLTRiMWMtOWY4NS05MjdmMmUyNTExYjIiLCJlbWFpbCI6InRlc3QxQGdtYWlsLmNvbSIsImV4cCI6MTY5ODg2MjkzMH0.0ATEbK6ZgjNHWNVYJMfW80i41ilH3VDQpqIhxbxi1-A"
    create_brain_data = {
        'name': 'expert2',
        'description': "test advisor",
        'prompt_id': None,
        'linkedin': "https://www.linkedin.com/in/test/",
        'extraversion': 0,
        'neuroticism': 0,
        'conscientiousness': 0
        }
    test_create_brain(token, create_brain_data)