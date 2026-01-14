def test_hello_query(client):
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


def test_kanji_query(client):
    response = client.post(
        "/graphql/",
        json={
            "query": """
                query {
                    kanji(literal: "猫") {
                        literal
                        meaning
                    }
                }
            """
        },
    )

    assert response.status_code == 200
