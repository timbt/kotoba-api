import os

from ariadne import QueryType, load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from dotenv import load_dotenv
from fastapi import FastAPI

from kotoba_api.util import kanjidic2_to_kanji

load_dotenv()

kanji = kanjidic2_to_kanji(os.getenv("KANJIDIC2_PATH"))

type_defs = load_schema_from_path("src/schema")

query = QueryType()


@query.field("hello")
def resolve_hello(*_):
    return "Hello world!"


@query.field("kanji")
def resolve_kanji(*_, literal=None):
    return {"literal": "猫", "meanings": [], "readings_on": [], "readings_kun": []}


# Create executable schema instance
schema = make_executable_schema(type_defs, query)

# Mount Ariadne GraphQL as sub-application for FastAPI
app = FastAPI()

app.mount("/graphql/", GraphQL(schema, debug=True))
