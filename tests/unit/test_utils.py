import xml.etree.ElementTree as ET

from kotoba_api.util import _parse_kanjidic2_element_to_kanji, kanjidic2_to_kanji

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


def test_parse_kanjidic2_element_to_kanji_parses_single_kanji():
    element = ET.fromstring(kanji_xml_neko)
    kanji = _parse_kanjidic2_element_to_kanji(element)
    assert kanji.literal == "猫"


def test_kanjidic2_to_kanji_parses_kanji():
    kanji = kanjidic2_to_kanji("tests/fixtures/kanjidic2.xml")
    assert kanji == []
