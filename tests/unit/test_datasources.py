import pytest

from kotoba_api.datasources.kanjidic import KanjiDic
from kotoba_api.models import Kanji

neko = Kanji(
    literal="猫",
    readings_on=("ビョウ",),
    readings_kun=("ねこ",),
    meanings=("cat",),
)
inu = Kanji(
    literal="犬",
    readings_on=("ケン",),
    readings_kun=("いぬ",),
    meanings=("dog",),
)


@pytest.fixture
def kanjidic():
    return KanjiDic([neko, inu])


def test_get_kanji_by_literal_returns_matching_kanji(kanjidic: KanjiDic):
    assert kanjidic.get_kanji_by_literal("猫") == neko


def test_get_kanji_by_literal_returns_none_for_unknown_literal(kanjidic: KanjiDic):
    assert kanjidic.get_kanji_by_literal("龍") is None


def test_get_kanji_by_literal_is_exact_match(kanjidic: KanjiDic):
    assert kanjidic.get_kanji_by_literal("猫 ") is None


def test_kanjidic_built_from_empty_list_returns_none():
    kanjidic = KanjiDic([])
    assert kanjidic.get_kanji_by_literal("猫") is None
