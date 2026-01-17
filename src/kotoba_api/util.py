import logging
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, ParseError

from kotoba_api.data_models import Kanji

logger = logging.getLogger(__name__)


class KanjiParsingException(Exception):
    """Custom exception for issues parsing KANJIDIC2 data"""

    pass


def _fetch_kanjidic2_from_fs(path: str) -> ET.ElementTree[Element[str]]:
    try:
        return ET.parse(path)
    except FileNotFoundError:
        logging.critical("Could not find specified KANJIDIC2 file %s" % path)
        raise
    except ParseError:
        logging.critical("Could not parse specified KANJIDIC2 file %s" % path)
        raise


def _parse_kanjidic2_element_to_kanji(element: Element) -> Kanji:
    """
    Parses a kanji XML element into a more friendly dataclass object.

    The expected input is an XML ElementTree Element corresponding to a 'character'
    element from a KANJIDIC2 file. Inputs lacking the expected subelements of a
    'character' element will cause the method to raise a KanjiParsingException.
    """
    # Parse Kanji literal
    literal_element = element.find("literal")
    if literal_element is None:
        raise KanjiParsingException("Missing 'literal' element")
    literal = literal_element.text
    if not literal:
        raise KanjiParsingException("Missing text field on 'literal' element")

    # Attempt to fetch readming_meaning element
    reading_meaning_element = element.find("reading_meaning")
    if reading_meaning_element is None:
        raise KanjiParsingException(
            "Missing 'reading_meaning' element in kanji entry for %s" % literal
        )

    readings_on: tuple[str, ...] = ()
    readings_kun: tuple[str, ...] = ()
    meanings: tuple[str, ...] = ()

    # Extract readings and meanings from any 'rmgroup' elements present
    for rmgroup_element in reading_meaning_element.findall("rmgroup"):
        for el in rmgroup_element:
            if (
                el.tag == "reading"
                and el.get("r_type")
                and el.get(key="r_type") == "ja_on"
            ):
                if el.text:
                    readings_on = readings_on + (el.text,)
            elif (
                el.tag == "reading"
                and el.get("r_type")
                and el.get(key="r_type") == "ja_kun"
            ):
                if el.text:
                    readings_kun = readings_kun + (el.text,)
            # Meaning elements are treated as english meanings if they have no 'm_lang' attribute
            # or if the m_lang attribute is explicitly set to "en"
            elif el.tag == "meaning" and (
                el.get("m_lang") is None
                or (el.get("m_lang") and el.get("m_lang") == "en")
            ):
                if el.text:
                    meanings = meanings + (el.text,)

    return Kanji(
        literal=literal,
        readings_on=readings_on,
        readings_kun=readings_kun,
        meanings=meanings,
    )


def kanjidic2_to_kanji(path: str | None) -> list[Kanji]:
    if path is None:
        logger.error("No KANJIDIC2 file specified. Is KANJIDIC2_PATH unset?")
        return []

    kanji: list[Kanji] = []

    etree = _fetch_kanjidic2_from_fs(path)
    for character_el in etree.findall("character"):
        try:
            character = _parse_kanjidic2_element_to_kanji(character_el)
        except KanjiParsingException as e:
            logging.info("Issue parsing kanji: %s" % e)
            character = None

        if character is not None:
            if len(character.readings_on) == 0 and len(character.readings_kun) == 0:
                logging.info("No readings found for character %s" % character.literal)
            if len(character.meanings) == 0:
                logging.info("No meanings found for character %s" % character.literal)
            kanji.append(character)

    return kanji
