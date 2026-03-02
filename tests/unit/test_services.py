from unittest.mock import MagicMock, create_autospec

import pytest

from kotoba_api.datasources.kanjidic import KanjiDic
from kotoba_api.models import Kanji
from kotoba_api.services import get_kanji_by_literal

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
