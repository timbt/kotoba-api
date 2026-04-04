from kotoba_api.models import Kanji


class KanjiDic:
    @staticmethod
    def _make_literal_index(kanji: list[Kanji]) -> dict[str, Kanji]:
        """
        Creates a lookup table to facilitate fetching characters by their literal value
        """
        index: dict[str, Kanji] = {}
        for character in kanji:
            index[character.literal] = character

        return index

    def __init__(self, kanji: list[Kanji]):
        self._kanji: list[Kanji] = kanji
        self._literal_index: dict[str, Kanji] = self._make_literal_index(kanji)

    def get_kanji_by_literal(self, literal: str) -> Kanji | None:
        """
        Returns the character corresponding to a given literal,
        or None if the character does not exist.
        """
        if literal in self._literal_index:
            return self._literal_index[literal]
        else:
            return None

    def search_kanji_by_meaning(self, meaning: str) -> list[Kanji]:
        """
        Returns a list of characters possessing meanings matching the provided meaning.

        Returns an empty list of no characters match.
        """

        return [k for k in self._kanji if meaning in k.meanings]

    def search_kanji_by_normalized_meaning(self, meaning: str) -> list[Kanji]:
        """
        Returns a list of characters possessing meanings matching the provided meaning.

        Both the provided search string and the meanings listed for the kanji will be
        normalized (stripped of leading and trailing whitespace and converted to
        lowercase) before the comparison is performed.

        Returns an empty list of no characters match.
        """

        matches: list[Kanji] = []
        for kanji in self._kanji:
            meanings: list[str] = [m.strip().lower() for m in kanji.meanings]
            if meaning.strip().lower() in meanings:
                matches.append(kanji)

        return matches
