from ariadne import QueryType, load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from fastapi import FastAPI

type_defs = load_schema_from_path("schema")

query = QueryType()


@query.field("hello")
def resolve_hello(*_):
    return "Hello world!"


# Create executable schema instance
schema = make_executable_schema(type_defs, query)

# Mount Ariadne GraphQL as sub-application for FastAPI
app = FastAPI()

app.mount("/graphql/", GraphQL(schema, debug=True))
