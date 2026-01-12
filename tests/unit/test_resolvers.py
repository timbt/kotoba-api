from kotoba_api.app import resolve_hello


def test_hello_resolver_returns_expected_string():
    result = resolve_hello(None, None)
    assert result == "Hello world!"
