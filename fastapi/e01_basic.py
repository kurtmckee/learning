"""
Learning about FastAPI <https://fastapi.tiangolo.com/>.

My goal is to understand several facets of FastAPI:

*   Doc generation at `/docs` and `/redoc` endpoints
    (including built-in "Try it out" functionality)
*   Return custom HTTP statuses.
*   Use path parameters.
*   Use models to load and validate input data.

The test runs well.

The command I used to actually launch this was:

..  code-block::

    uvicorn e01_basic:app --reload

"""

import enum
import itertools

import fastapi
import pydantic


class State(str, enum.Enum):
    OR = "OR"
    WA = "WA"
    CA = "CA"


class Town(pydantic.BaseModel):
    id: int = pydantic.Field(default_factory=itertools.count(1).__next__)
    name: pydantic.constr(min_length=1)
    state: State
    population: pydantic.conint(strict=True, ge=1)


towns_raw = [
    Town(name="Salem", state=State.OR, population=175_535),
    Town(name="Olympia", state=State.WA, population=51_534),
    Town(name="Sacramento", state=State.CA, population=500_930),
]

towns = {town.id: town for town in towns_raw}


app = fastapi.FastAPI()


@app.get("/")
async def show_all_towns():
    return {"towns": list(towns.values())}


@app.post("/add", status_code=fastapi.status.HTTP_201_CREATED)
async def add_town(town: Town, response: fastapi.Response):
    if town.id in towns:
        response.status_code = fastapi.status.HTTP_409_CONFLICT
        return {"error": f"Town ID {town.id} already exists"}
    towns[town.id] = town
    return "OK"


@app.get("/{town_id:int}")
async def get_town_info(town_id: int, response: fastapi.Response):
    if town_id not in towns:
        response.status_code = fastapi.status.HTTP_404_NOT_FOUND
        return {"error": f"Town ID {town_id} not found"}
    return towns[town_id]


@app.put("/{town_id:int}/edit", status_code=fastapi.status.HTTP_202_ACCEPTED)
async def update_town(town_id: int, town: Town, response: fastapi.Response):
    if town_id not in towns:
        response.status_code = fastapi.status.HTTP_404_NOT_FOUND
        return {"error": f"Town ID {town_id} not found"}

    town.id = town_id
    towns[town.id] = town
    return "OK"
