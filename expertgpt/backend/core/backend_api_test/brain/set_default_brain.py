import requests

ENDPOINT = "http://localhost:5051"

def test_set_default_brain(token, brain_id):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(url=ENDPOINT+f'/brains/{brain_id}/default/', headers=headers)
    print(f"status_code: {response.status_code}, \ttext: {response.text}")

if __name__ == '__main__':
    token = ""
    brain_id = ""
    test_set_default_brain(token, brain_id)