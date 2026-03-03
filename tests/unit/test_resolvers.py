from unittest.mock import ANY, patch

from kotoba_api.app import resolve_hello, resolve_kanji
from kotoba_api.models import Kanji

neko = Kanji(
    literal="猫",
    readings_on=("ビョウ",),
    readings_kun=("ねこ",),
    meanings=("cat",),
)


def test_hello_resolver_returns_expected_string():
    result = resolve_hello(None, None)
    assert result == "Hello world!"


@patch("kotoba_api.app.get_kanji_by_literal")
def test_kanji_resolver_returns_none_when_literal_is_none(mock_service):
    assert resolve_kanji(None, None) is None
    mock_service.assert_not_called()


@patch("kotoba_api.app.get_kanji_by_literal")
def test_kanji_resolver_delegates_to_service(mock_service):
    mock_service.return_value = neko
    assert resolve_kanji(None, None, literal="猫") == neko


@patch("kotoba_api.app.get_kanji_by_literal")
def test_kanji_resolver_passes_literal_to_service(mock_service):
    resolve_kanji(None, None, literal="猫")
    mock_service.assert_called_once_with(ANY, "猫")
