import logging
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

from kotoba_api.data_models import Kanji

logger = logging.getLogger(__name__)


def _fetch_kanjidic2_from_fs(path: str):
    try:
        return ET.parse(path)
    except FileNotFoundError:
        logging.critical("Could not find specified kanjidic2 file %s" % path)
        raise
    except ParseError:
        logging.critical("Could not parse specified kanjidic2 file %s" % path)
        raise


def kanjidic2_to_kanji(path: str | None) -> list[Kanji]:
    if path is None:
        logger.error("No KANJIDIC2 file specified. Is KANJIDIC2_PATH unset?")
        return []

    return []
