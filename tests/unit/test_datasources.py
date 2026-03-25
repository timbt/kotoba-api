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
kawa1 = Kanji(
    literal="川",
    readings_on=("セン",),
    readings_kun=("かわ",),
    meanings=("stream", "river"),
)
kawa2 = Kanji(
    literal="河",
    readings_on=("カ",),
    readings_kun=("かわ",),
    meanings=("river",),
)


@pytest.fixture
def kanjidic():
    return KanjiDic([neko, inu, kawa1, kawa2])


def test_get_kanji_by_literal_returns_matching_kanji(kanjidic: KanjiDic):
    assert kanjidic.get_kanji_by_literal("猫") == neko


def test_get_kanji_by_literal_returns_none_for_unknown_literal(kanjidic: KanjiDic):
    assert kanjidic.get_kanji_by_literal("龍") is None


def test_get_kanji_by_literal_is_exact_match(kanjidic: KanjiDic):
    assert kanjidic.get_kanji_by_literal("猫 ") is None


def test_kanjidic_built_from_empty_list_returns_none():
    kanjidic = KanjiDic([])
    assert kanjidic.get_kanji_by_literal("猫") is None


@pytest.mark.xfail(reason="Not yet implemented", strict=True)
def test_search_kanji_by_meaning(kanjidic: KanjiDic):
    assert kanjidic.search_kanji_by_meaning("cat") == [neko]


@pytest.mark.xfail(reason="Not yet implemented", strict=True)
def test_search_kanji_by_meaning_with_multiple_results(kanjidic: KanjiDic):
    results = kanjidic.search_kanji_by_meaning("river")
    assert kawa1 in results
    assert kawa2 in results


@pytest.mark.xfail(reason="Not yet implemented", strict=True)
def test_search_kanji_by_unknown_meaning(kanjidic: KanjiDic):
    assert kanjidic.search_kanji_by_meaning("foobarbat") == []
