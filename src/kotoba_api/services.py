from kotoba_api.datasources.kanjidic import KanjiDic
from kotoba_api.models import Kanji


def get_kanji_by_literal(kanjidic: KanjiDic, literal: str) -> Kanji | None:
    return kanjidic.get_kanji_by_literal(literal)
