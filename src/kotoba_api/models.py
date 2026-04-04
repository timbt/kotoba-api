from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Kanji:
    literal: str
    readings_on: tuple[str, ...]
    readings_kun: tuple[str, ...]
    meanings: tuple[str, ...]


@dataclass
class SearchResults:
    search_query: str
    kanji: list[Kanji]
