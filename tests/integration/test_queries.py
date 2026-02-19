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


def test_kanji_query(client: TestClient):
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
