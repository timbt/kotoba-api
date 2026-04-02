import pytest
from fastapi.testclient import TestClient


def test_hello_query(client: TestClient):
    response = client.post(
        "/graphql/",
        json={
            "query": """
                query {
                    hello
                }
            """
        },
    )

    assert response.status_code == 200

    payload = response.json()
    assert "errors" not in payload
    assert payload["data"]["hello"] == "Hello world!"


def test_kanji_query_by_literal(client: TestClient):
    response = client.post(
        "/graphql/",
        json={
            "query": """
                query {
                    kanji(literal: "猫") {
                        literal
                        readings_on
                        readings_kun
                        meanings
                    }
                }
            """
        },
    )

    assert response.status_code == 200

    payload = response.json()
    assert "errors" not in payload
    assert payload["data"]["kanji"]["literal"] == "猫"
    assert "ビョウ" in payload["data"]["kanji"]["readings_on"]
    assert "ねこ" in payload["data"]["kanji"]["readings_kun"]
    assert "cat" in payload["data"]["kanji"]["meanings"]


def test_kanji_query_returns_null_for_unknown_literal(client: TestClient):
    response = client.post(
        "/graphql/",
        json={"query": 'query { kanji(literal: "龍") { literal } }'},
    )

    assert response.status_code == 200

    payload = response.json()
    assert "errors" not in payload
    assert payload["data"]["kanji"] is None


def test_kanji_search_by_meaning(client: TestClient):
    response = client.post(
        "/graphql/",
        json={
            "query": """
                query {
                    kanjiByMeaning(meaning: "cat") {
                        literal
                        readings_on
                        readings_kun
                        meanings
                    }
                }
            """
        },
    )

    assert response.status_code == 200

    payload = response.json()
    kanji_list = payload["data"]["kanjiByMeaning"]
    assert len(kanji_list) > 0

    neko = next(k for k in kanji_list if k["literal"] == "猫")
    assert "ビョウ" in neko["readings_on"]
    assert "ねこ" in neko["readings_kun"]
    assert "cat" in neko["meanings"]


@pytest.mark.xfail(reason="Feature not yet implemented", strict=True)
def test_search_query_search_by_literal(client: TestClient):
    response = client.post(
        "/graphql/",
        json={
            "query": """"
                query {
                    search(searchQuery: "猫") {
                        searchQuery
                        kanji {
                            literal
                            readings_on
                            readings_kun
                            meanings
                        }
                    }
                }
            """
        },
    )

    assert response.status_code == 200

    payload = response.json()

    # Verify correct query was used in search
    assert payload["data"]["meaning"] == "猫"
