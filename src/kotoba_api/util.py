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


def _parse_kanjidic2_element_to_kanji(el: Element) -> Kanji:
    """
    Parses a kanji XML element into a more friendly dataclass object.

    The expected input is an XML ElementTree Element corresponding to a 'character'
    element from a KANJIDIC2 file. Inputs lacking the expected subelements of a
    'character' element will cause the method to raise a KanjiParsingException.
    """
    literalElement = el.find("literal")
    if literalElement is None:
        raise KanjiParsingException("Missing 'literal' element")
    literal = literalElement.text
    if not literal:
        raise KanjiParsingException("Missing text field on 'literal' element")

    return Kanji(literal=literal, readings_on=(), readings_kun=(), meanings=())


def kanjidic2_to_kanji(path: str | None) -> list[Kanji]:
    if path is None:
        logger.error("No KANJIDIC2 file specified. Is KANJIDIC2_PATH unset?")
        return []

    etree = _fetch_kanjidic2_from_fs(path)

    return []
