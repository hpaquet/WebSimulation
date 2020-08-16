import numpy as np
import pandas as pd
import scipy.constants as constants

from simulationservice.provider.dataprovider import DataProvider


class BlackBodySpectrum(DataProvider):

    def __init__(self, temperature):
        super().__init__()

        if temperature:
            self.temperature = temperature
        else:
            raise ValueError('Temperature need to be defined')

        self.x = pd.Series(np.linspace(start=0, stop=3e-6, num=1000))  # wavelenght

    def get_arg(self):
        pass

    def compute(self):
        c = constants.c
        h = constants.h
        Kb = constants.Boltzmann
        l = self.x  # wavelenght
        T = self.temperature

        self.y = ( 2*h*np.power(c, 2) ) / ( np.power(l, 5) * ( np.exp((h*c) / (l*Kb*T))-1 ) )*1e-12
        self.x = self.x*1e6
