import xml.etree.ElementTree as ET
from unittest.mock import patch

import pytest

from kotoba_api.util import (
    KanjiParsingException,
    _parse_kanjidic2_element_to_kanji,
    kanjidic2_to_kanji,
)

kanji_xml_neko = """<character>
<literal>猫</literal>
<codepoint>
<cp_value cp_type="ucs">732b</cp_value>
<cp_value cp_type="jis208">1-39-13</cp_value>
</codepoint>
<radical>
<rad_value rad_type="classical">94</rad_value>
</radical>
<misc>
<grade>8</grade>
<stroke_count>11</stroke_count>
<variant var_type="jis212">1-63-05</variant>
<freq>1702</freq>
<jlpt>2</jlpt>
</misc>
<dic_number>
<dic_ref dr_type="nelson_c">2893</dic_ref>
<dic_ref dr_type="nelson_n">3586</dic_ref>
<dic_ref dr_type="halpern_njecd">535</dic_ref>
<dic_ref dr_type="halpern_kkd">651</dic_ref>
<dic_ref dr_type="halpern_kkld">391</dic_ref>
<dic_ref dr_type="halpern_kkld_2ed">488</dic_ref>
<dic_ref dr_type="heisig">244</dic_ref>
<dic_ref dr_type="heisig6">259</dic_ref>
<dic_ref dr_type="gakken">1763</dic_ref>
<dic_ref dr_type="oneill_names">1304</dic_ref>
<dic_ref dr_type="moro" m_vol="7" m_page="0719">20535X</dic_ref>
<dic_ref dr_type="henshall">1742</dic_ref>
<dic_ref dr_type="sh_kk">1470</dic_ref>
<dic_ref dr_type="sh_kk2">1567</dic_ref>
<dic_ref dr_type="jf_cards">730</dic_ref>
<dic_ref dr_type="tutt_cards">1461</dic_ref>
<dic_ref dr_type="kanji_in_context">1410</dic_ref>
<dic_ref dr_type="kodansha_compact">1304</dic_ref>
<dic_ref dr_type="maniette">250</dic_ref>
</dic_number>
<query_code>
<q_code qc_type="skip">1-3-8</q_code>
<q_code qc_type="sh_desc">3g8.5</q_code>
<q_code qc_type="four_corner">4426.0</q_code>
<q_code qc_type="deroo">2976</q_code>
</query_code>
<reading_meaning>
<rmgroup>
<reading r_type="pinyin">mao1</reading>
<reading r_type="pinyin">mao2</reading>
<reading r_type="korean_r">myo</reading>
<reading r_type="korean_h">묘</reading>
<reading r_type="vietnam">Miêu</reading>
<reading r_type="ja_on">ビョウ</reading>
<reading r_type="ja_kun">ねこ</reading>
<meaning>cat</meaning>
<meaning m_lang="fr">chat</meaning>
<meaning m_lang="es">gato</meaning>
<meaning m_lang="pt">Gato</meaning>
</rmgroup>
</reading_meaning>
</character>
"""


def _make_etree(xml_string: str) -> ET.ElementTree:
    return ET.ElementTree(ET.fromstring(xml_string))


# _parse_kanjidic2_element_to_kanji


def test_parse_kanjidic2_element_to_kanji_parses_single_kanji():
    element = ET.fromstring(kanji_xml_neko)
    kanji = _parse_kanjidic2_element_to_kanji(element)
    assert kanji.literal == "猫"
    assert kanji.readings_on == ("ビョウ",)
    assert kanji.readings_kun == ("ねこ",)
    assert kanji.meanings == ("cat",)


def test_parse_kanjidic2_element_raises_when_literal_missing():
    element = ET.fromstring("<character><reading_meaning/></character>")
    with pytest.raises(KanjiParsingException):
        _parse_kanjidic2_element_to_kanji(element)


def test_parse_kanjidic2_element_raises_when_reading_meaning_missing():
    element = ET.fromstring("<character><literal>猫</literal></character>")
    with pytest.raises(KanjiParsingException):
        _parse_kanjidic2_element_to_kanji(element)


# kanjidic2_to_kanji


def test_kanjidic2_to_kanji_returns_empty_list_when_path_is_none():
    assert kanjidic2_to_kanji(None) == []


@patch("kotoba_api.util._fetch_kanjidic2_from_fs")
def test_kanjidic2_to_kanji_parses_first_kanji(mock_fetch):
    mock_fetch.return_value = _make_etree("""<kanjidic2>
        <character>
            <literal>亜</literal>
            <reading_meaning>
                <rmgroup>
                    <reading r_type="ja_on">ア</reading>
                    <reading r_type="ja_kun">つ.ぐ</reading>
                    <meaning>Asia</meaning>
                    <meaning>rank next</meaning>
                    <meaning>come after</meaning>
                    <meaning>-ous</meaning>
                </rmgroup>
            </reading_meaning>
        </character>
    </kanjidic2>""")

    kanji = kanjidic2_to_kanji("any/path")

    assert kanji[0].literal == "亜"
    assert kanji[0].readings_on == ("ア",)
    assert kanji[0].readings_kun == ("つ.ぐ",)
    assert kanji[0].meanings == ("Asia", "rank next", "come after", "-ous")


@patch("kotoba_api.util._fetch_kanjidic2_from_fs")
def test_kanjidic2_to_kanji_skips_invalid_elements(mock_fetch):
    mock_fetch.return_value = _make_etree("""<kanjidic2>
        <character>
            <literal>猫</literal>
            <reading_meaning>
                <rmgroup>
                    <reading r_type="ja_on">ビョウ</reading>
                    <reading r_type="ja_kun">ねこ</reading>
                    <meaning>cat</meaning>
                </rmgroup>
            </reading_meaning>
        </character>
        <character>
            <literal>犬</literal>
            <reading_meaning>
                <rmgroup>
                    <reading r_type="ja_on">ケン</reading>
                    <reading r_type="ja_kun">いぬ</reading>
                    <meaning>dog</meaning>
                </rmgroup>
            </reading_meaning>
        </character>
        <character>
            <literal>一</literal>
        </character>
    </kanjidic2>""")

    kanji = kanjidic2_to_kanji("any/path")

    assert len(kanji) == 2
