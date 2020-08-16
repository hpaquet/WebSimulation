from enum import Enum
from typing import Optional

from fastapi import FastAPI, Path, Query

import settings
import simulations as sim

service = FastAPI(title=settings.SERVICE_TITLE)


Parameters = [
    'wavelenght',
    'temperature'
]


@service.get("/")
async def read_data():

    return {"message": "Main route"}


@service.get("/{simulation_id}")
async def read_data(simulation_id: str, temperature: Optional[int] = Query(None, alias='Temperature')):

    if hasattr(sim, simulation_id):
        data_provider = getattr(sim, simulation_id)(temperature)

        return data_provider.get_data()

    return {"message": "Simulation ID not available"}