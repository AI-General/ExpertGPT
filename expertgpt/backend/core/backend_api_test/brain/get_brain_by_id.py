import requests

ENDPOINT = "http://localhost:5051"

def test_get_brain_by_id(token, brain_id):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url=ENDPOINT+f'/brains/{brain_id}/', headers=headers)
    print(f"status_code: {response.status_code}, \ttext: {response.text}")

if __name__ == '__main__':
    token = ""
    brain_id = ""
    test_get_brain_by_id(token, brain_id)