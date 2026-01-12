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
