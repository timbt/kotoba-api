from kotoba_api.datasources.kanjidic import KanjiDic
from kotoba_api.models import Kanji, SearchResults


def get_kanji_by_literal(kanjidic: KanjiDic, literal: str) -> Kanji | None:
    return kanjidic.get_kanji_by_literal(literal)


def search_kanji_by_meaning(kanjidic: KanjiDic, meaning: str) -> list[Kanji]:
    return kanjidic.search_kanji_by_meaning(meaning)


def search(kanjidic: KanjiDic, search_query: str) -> SearchResults:
    kanji_results: list[Kanji] = []

    literal_result = kanjidic.get_kanji_by_literal(search_query)
    if literal_result:
        kanji_results.append(literal_result)

    kanji_results.extend(kanjidic.search_kanji_by_meaning(search_query))

    return SearchResults(search_query=search_query, kanji=kanji_results)
