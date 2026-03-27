import os

from ariadne import QueryType, load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kotoba_api.datasources.kanjidic import KanjiDic
from kotoba_api.services import get_kanji_by_literal, search_kanji_by_meaning
from kotoba_api.util import kanjidic2_to_kanji

load_dotenv()

kanji = kanjidic2_to_kanji(os.getenv("KANJIDIC2_PATH"))
kanjidic = KanjiDic(kanji)
type_defs = load_schema_from_path("src/schema")

query = QueryType()


@query.field("hello")
def resolve_hello(*_):
    return "Hello world!"


@query.field("kanji")
def resolve_kanji(*_, literal=None):
    if literal is None:
        return None
    return get_kanji_by_literal(kanjidic, literal)


@query.field(name="kanjiByMeaning")
def resolve_kanji_by_meaning(*_, meaning=None):
    if meaning is None:
        return None
    return search_kanji_by_meaning(kanjidic, meaning)


# Create executable schema instance
schema = make_executable_schema(type_defs, query)

# Mount Ariadne GraphQL as sub-application for FastAPI
app = FastAPI()

# Configure CORS
origins = ["https://timbt.github.io", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,  # ty:ignore[invalid-argument-type]
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
)

app.mount("/graphql/", GraphQL(schema, debug=True))
