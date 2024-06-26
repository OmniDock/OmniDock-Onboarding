# otto/api.py

import time
import requests
from dotenv import dotenv_values

class OttoAPIWrapper:
    def __init__(self):
        # Load environment variables from .env file
        env = dotenv_values()
        self.client_id = env['OTTO_SANDBOX_CLIENT_ID']
        self.client_secret = env['OTTO_SANDBOX_CLIENT_SECRET']
        self.base_url = 'https://sandbox.api.otto.market'
        self.access_token = None

    def authenticate(self):
        auth_url = f"{self.base_url}/v1/token"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'orders products'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(auth_url, data=payload, headers=headers)
        if response.status_code == 200:
            self.access_token = response.json().get('access_token')
        else:
            raise Exception(f"Failed to authenticate. Status code: {response.status_code}")

    def get_orders(self, query_params=None):
        if not self.access_token:
            self.authenticate()

        url = f"{self.base_url}/v4/orders"
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = requests.get(url, headers=headers, params=query_params)
        while True:
            if response.status_code == 429:  # Rate limit exceeded
                    retry_after = int(response.headers.get('Retry-After', 1))
                    time.sleep(retry_after)
            elif response.status_code == 200:
                return response.json().get('resources', [])
            else:
                raise Exception(f"Failed to fetch orders. Status code: {response.status_code}")
        


