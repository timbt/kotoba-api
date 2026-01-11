from kotoba_api.app import resolve_hello


def test_resolve_hello():
    result = resolve_hello(None, None)
    assert result == "Hello world!"
