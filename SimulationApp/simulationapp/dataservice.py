import os
import requests
import json

import pandas as pd


class DataServiceClient:

    def __init__(self):
        self.data = None

        self.service_url = os.environ.get('SERVICE_URL')

        if not self.service_url:
            raise ValueError('SERVICE_URL not available')

    def _get_request(self, url):
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()

        return None

    def get_data(self, simulation_id, **parameters):

        args = []
        for k, v in parameters.items():
            args += [f"{k}={v}"]

        url = f"{self.service_url}/{simulation_id}?{'&'.join(args)}"
        data = self._get_request(url)

        return pd.read_json(data)


if __name__ == '__main__':

    simulation = 'BlackBodySpectrum'

    client = DataServiceClient()

    data = client.get_data(simulation, Temperature=5000)


