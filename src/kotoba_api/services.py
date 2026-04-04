from kotoba_api.datasources.kanjidic import KanjiDic
from kotoba_api.models import Kanji, SearchResults


def get_kanji_by_literal(kanjidic: KanjiDic, literal: str) -> Kanji | None:
    return kanjidic.get_kanji_by_literal(literal)


def search_kanji_by_meaning(
    kanjidic: KanjiDic, meaning: str, normalize=False
) -> list[Kanji]:
    return (
        kanjidic.search_kanji_by_normalized_meaning(meaning)
        if normalize
        else kanjidic.search_kanji_by_meaning(meaning)
    )


def search(kanjidic: KanjiDic, search_query: str) -> SearchResults:
    seen_kanji: set[Kanji] = set()
    kanji_results: list[Kanji] = []

    def add_if_unseen_kanji(kanji: Kanji) -> None:
        if kanji not in seen_kanji:
            seen_kanji.add(kanji)
            kanji_results.append(kanji)

    literal_result = kanjidic.get_kanji_by_literal(search_query)
    if literal_result:
        add_if_unseen_kanji(literal_result)

    for k in kanjidic.search_kanji_by_normalized_meaning(search_query):
        if k not in kanji_results:
            kanji_results.append(k)

    return SearchResults(search_query=search_query, kanji=kanji_results)
