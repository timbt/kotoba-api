from unittest.mock import MagicMock, create_autospec

import pytest

from kotoba_api.datasources.kanjidic import KanjiDic
from kotoba_api.models import Kanji
from kotoba_api.services import get_kanji_by_literal, search, search_kanji_by_meaning

neko = Kanji(
    literal="猫",
    readings_on=("ビョウ",),
    readings_kun=("ねこ",),
    meanings=("cat",),
)


@pytest.fixture
def kanjidic() -> MagicMock:
    return create_autospec(KanjiDic)


def test_get_kanji_by_literal_returns_kanji_from_datasource(kanjidic: MagicMock):
    kanjidic.get_kanji_by_literal.return_value = neko
    assert get_kanji_by_literal(kanjidic, "猫") == neko


def test_get_kanji_by_literal_returns_none_from_datasource(kanjidic: MagicMock):
    kanjidic.get_kanji_by_literal.return_value = None
    assert get_kanji_by_literal(kanjidic, "龍") is None


def test_get_kanji_by_literal_passes_literal_to_datasource(kanjidic: MagicMock):
    get_kanji_by_literal(kanjidic, "猫")
    kanjidic.get_kanji_by_literal.assert_called_once_with("猫")


def test_search_kanji_by_meaning_returns_list_from_datasource(kanjidic: MagicMock):
    kanjidic.search_kanji_by_meaning.return_value = [neko]
    assert search_kanji_by_meaning(kanjidic, "cat") == [neko]


def test_search_kanji_by_meaning_returns_empty_list_when_no_matches(
    kanjidic: MagicMock,
):
    kanjidic.search_kanji_by_meaning.return_value = []
    assert search_kanji_by_meaning(kanjidic, "asdf") == []


def test_search_kanji_by_meaning_passes_meaning_to_datasource(kanjidic: MagicMock):
    search_kanji_by_meaning(kanjidic, "cat")
    kanjidic.search_kanji_by_meaning.assert_called_once_with("cat")


def test_search_kanji_by_meaning_uses_normalized_datasource_method_when_normalize_is_true(
    kanjidic: MagicMock,
):
    kanjidic.search_kanji_by_normalized_meaning.return_value = [neko]
    assert search_kanji_by_meaning(kanjidic, "Cat", normalize=True) == [neko]
    kanjidic.search_kanji_by_normalized_meaning.assert_called_once_with("Cat")
    kanjidic.search_kanji_by_meaning.assert_not_called()


def test_search_kanji_by_meaning_uses_standard_datasource_method_when_normalize_is_false(
    kanjidic: MagicMock,
):
    kanjidic.search_kanji_by_meaning.return_value = [neko]
    assert search_kanji_by_meaning(kanjidic, "cat", normalize=False) == [neko]
    kanjidic.search_kanji_by_meaning.assert_called_once_with("cat")
    kanjidic.search_kanji_by_normalized_meaning.assert_not_called()


def test_search_service_returns_empty_list_for_empty_search_string(kanjidic: MagicMock):
    kanjidic.get_kanji_by_literal.return_value = None
    kanjidic.search_kanji_by_meaning.return_value = []

    result = search(kanjidic, "")

    assert result.search_query == ""
    assert result.kanji == []


def test_search_returns_single_kanji_for_literal_query(kanjidic: MagicMock):
    kanjidic.get_kanji_by_literal.return_value = neko
    kanjidic.search_kanji_by_meaning.return_value = []

    result = search(kanjidic, "猫")

    assert result.search_query == "猫"
    assert result.kanji == [neko]


def test_search_returns_kanji_for_search_by_meaning(kanjidic: MagicMock):
    kanjidic.get_kanji_by_literal.return_value = None
    kanjidic.search_kanji_by_meaning.return_value = [neko]

    result = search(kanjidic, "猫")

    assert result.search_query == "猫"
    assert result.kanji == [neko]


def test_search_does_not_return_duplicate_kanji(kanjidic: MagicMock):
    kanjidic.get_kanji_by_literal.return_value = neko
    kanjidic.search_kanji_by_meaning.return_value = [neko]

    result = search(kanjidic, "猫")

    assert result.search_query == "猫"
    assert result.kanji == [neko]
