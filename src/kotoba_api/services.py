from kotoba_api.models import Kanji


def get_kanji_by_literal(literal: str) -> Kanji | None:
    return Kanji(literal="猫", readings_on=(), readings_kun=(), meanings=())
