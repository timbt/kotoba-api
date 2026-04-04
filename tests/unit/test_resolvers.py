from unittest.mock import ANY, patch

from kotoba_api.app import (
    resolve_hello,
    resolve_kanji,
    resolve_kanji_by_meaning,
    resolve_search,
)
from kotoba_api.models import Kanji, SearchResults

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
def test_kanji_resolver_delegates_to_service(mock_service):
    mock_service.return_value = neko
    assert resolve_kanji(None, None, literal="猫") == neko


@patch("kotoba_api.app.get_kanji_by_literal")
def test_kanji_resolver_passes_literal_to_service(mock_service):
    resolve_kanji(None, None, literal="猫")
    mock_service.assert_called_once_with(ANY, "猫")


@patch("kotoba_api.app.search_kanji_by_meaning")
def test_kanji_by_meaning_resolver_delegates_to_service(mock_service):
    mock_service.return_value = [neko]
    assert resolve_kanji_by_meaning(None, None, meaning="cat") == [neko]


@patch("kotoba_api.app.search_kanji_by_meaning")
def test_kanji_by_meaning_resolver_passes_meaning_to_service(mock_service):
    resolve_kanji_by_meaning(None, None, meaning="cat")
    mock_service.assert_called_once_with(ANY, "cat")


@patch("kotoba_api.app.search")
def test_search_resolver_delegates_to_service(mock_service):
    expected = SearchResults(search_query="猫", kanji=[neko])
    mock_service.return_value = expected
    assert resolve_search(None, None, searchQuery="猫") == expected


@patch("kotoba_api.app.search")
def test_search_resolver_passes_search_query_to_service(mock_service):
    resolve_search(None, None, searchQuery="猫")
    mock_service.assert_called_once_with(ANY, "猫")
