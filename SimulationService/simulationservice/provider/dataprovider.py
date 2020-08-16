from abc import abstractmethod
import json

import pandas as pd


class DataProvider:
    def __init__(self):
        self.y = None
        self.x = None

    @abstractmethod
    def compute(self):
        pass

    def get_data(self):

        self.compute()

        df = pd.DataFrame()
        df['y'] = self.y
        df['x'] = self.x

        return df.to_json()
