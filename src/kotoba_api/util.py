import logging
from xml.etree.ElementTree import ElementTree, ParseError

from kotoba_api.data_models import Kanji

logger = logging.getLogger(__name__)


def fetch_kanjidic2(path: str) -> ElementTree:
    try:
        return ElementTree().parse(path)
    except FileNotFoundError:
        logging.critical("Could not find specified kanjidic2 file %s" % path)
        raise
    except ParseError:
        logging.critical("Could not parse specified kanjidic2 file %s" % path)
        raise


def kanjidic2_to_kanji(kanjidic2tree: ElementTree) -> list[Kanji]:
    pass
