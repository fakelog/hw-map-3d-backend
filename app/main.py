from deta import Deta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from os import getenv
from pydantic import BaseModel

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
deta = Deta(getenv('DETA_BASE_PROJECT_KEY'))
db = deta.Base("routes")


class Connections(BaseModel):
    routes: list


def get_connections(key: str):
    return db.get(key)


def put_connections(data: list):
    fetch_routes = db.fetch(query={'value': data}, limit=1)
    if fetch_routes.count > 0:
        return fetch_routes.items[0]
    return db.put(data)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post('/routes/add')
def read_connections_add(connections: Connections):
    routes = put_connections(connections.routes)
    return routes


@app.get("/routes/{connections_id}")
def read_connections(connections_id: str):
    return get_connections(connections_id)
