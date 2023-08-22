import unittest
import connexion
import json
import requests
import os
import dotenv
import logger
from fastapi import UploadFile
from fastapi.testclient import TestClient
import pytest

logger = logger.get_logger(__name__)

# @pytest.fixture
# def client():
#     return TestClient(app)


class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.endpoint = "http://walletgpt.info:5050"
        # Retrieve/Replace this with your actual token 
        cls.token = "eyJhbGciOiJIUzI1NiIsImtpZCI6IldYODRPd0RUVUxhWmxtUjIiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNjkyNzI3Mjg3LCJpYXQiOjE2OTI3MjM2ODcsImlzcyI6Imh0dHBzOi8vbWRwdnRiaXZ4bmRjY2ZjZHJqaGQuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6IjNkYjgzM2E1LTY4OWUtNDIwNC1iMGNhLTgzN2JkZjRiYTJhZCIsImVtYWlsIjoiaG9uZ3l1eGlhbzA1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiLCJnb29nbGUiXX0sInVzZXJfbWV0YWRhdGEiOnsiYXZhdGFyX3VybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FBY0hUdGNhYUhYMS1rUUlMUWZWd0RKNjhaMmxVT3ViVkFaNHJsQkp5SHh3dXJNVz1zOTYtYyIsImVtYWlsIjoiaG9uZ3l1eGlhbzA1QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmdWxsX25hbWUiOiJIb25neXUgWGlhbyIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbSIsIm5hbWUiOiJIb25neXUgWGlhbyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQWNIVHRjYWFIWDEta1FJTFFmVndESjY4WjJsVU91YlZBWjRybEJKeUh4d3VyTVc9czk2LWMiLCJwcm92aWRlcl9pZCI6IjExNTU0NjIxMTk3NTUwNjcxNDUxOSIsInN1YiI6IjExNTU0NjIxMTk3NTUwNjcxNDUxOSJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6Im9hdXRoIiwidGltZXN0YW1wIjoxNjkyNjgwODgwfV0sInNlc3Npb25faWQiOiI0YjhjMGZlMi03NjI1LTQxYzItOGZmZi1iMTFiNjc4MmQxMGQifQ.dtEXkp9zfZqO-pQyxhiw8dUl-NMOp8yh5p0XlDBDdM8" 
        cls.headers = {
            'Authorization': f'Bearer {cls.token}'
            }

    """
    # Create new brain
    def test_post_brains(self):
        headers = {**self.headers, "Content-Type": "application/json"}

        data = {
            'description': "unittest",
            'name': 'unittest brain',
            'model': 'gpt-3.5-turbo-0613',
            'max_tokens': 378,
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'temperature': '0.75',
            'prompt_id': None,
            'extraversion': 3,
            'neuroticism': 0,
            'conscientiousness': 3
        }
        
        response = requests.post(self.endpoint + '/brains/', json=data, headers=headers)
        
        # self.assert_(response.status_code == 200 
        #              or response.status_code == 401
        #              or response.status_code == 429)
        logger.info('test_post_brains')
        logger.info(f"status_code: {response.status_code}, \ttext: {response.text}")

    # Upload knowledge
    def test_post_upload(self):
        headers = {**self.headers}  # "Content-Type": "multipart/form-data"
        params = {
            'brain_id': 'b8d1e86b-7e22-4c9f-96d2-14f01bf5d1d3'
            }
        
        file_path = '/root/hongyu/customersupportgpt/quivr_project/backend/core/unittest-upload.txt'
        assert os.path.exists(file_path)
        with open(file_path, 'rb') as f:
            
            files = {
                'uploadFile': f  # creates a FileStorage object with the file's content and filename.
            }

            response = requests.post(self.endpoint+'/upload', params=params, headers=headers, files=files)
            
            logger.info('test_post_brains')
            logger.info(f"status_code: {response.status_code}, \ttext: {response.text}")
    """
            
    # Chat with Brain
    def test_post_chat(self):
        headers = {**self.headers,  "Content-Type": "application/json"}
        chat_id = "6b14af62-608a-4787-b21c-3a48a0352897"
        params = {
            'brain_id': 'b8d1e86b-7e22-4c9f-96d2-14f01bf5d1d3'
        }
        data = {
            'question': "How about your personality?"
        }

        response = requests.post(
            url=self.endpoint+f'/chat/{chat_id}/question/stream', 
            headers=headers,
            params=params,
            json=data
        )

        logger.info('test_post_chat')
        logger.info(f"status_code: {response.status_code}, \ttext: {response.text}")
    
    # def test_get_chat_history(self):
    #     headers = {'Authorization': f'Bearer {self.token}'}
    #     response = self.client.get('/chat/{chat_id}/history', headers=headers)
    #     self.assertEqual(response.status_code, 200)
    #     # Add more assertions here based on the expected output/response

    # def test_crawl(self):
    #     headers = {'Authorization': f'Bearer {self.token}'}
    #     response = self.client.get('/your/crawl/endpoint', headers=headers)
    #     self.assertEqual(response.status_code, 200)

    # Add more test cases for each endpoint

if __name__ == '__main__':
    dotenv.load_dotenv()
    unittest.main()
