import pytest

from sinatools.morphology import morph_analyzer


def test_analyze_example():
    assert morph_analyzer.analyze("ذهب الولد الى المدرسة") == [
        {
            "token": "ذهب",
            "lemma": "ذَهَبَ | ذَهَبَ إلى | ذَهَبَ ب | ذَهَبَ على | ذَهَبَ عن | ذَهَبَ في",
            "lemma_id": 202001617,
            "root": "ذ ه ب",
            "pos": "فعل",
            "frequency": 349890,
        },
        {
            "token": "الولد",
            "lemma": "وَلَدٌ",
            "lemma_id": 202003092,
            "root": "و ل د",
            "pos": "اسم",
            "frequency": 320244,
        },
        {
            "token": "الى",
            "lemma": "إِلَى",
            "lemma_id": 202000856,
            "root": "إ ل ى",
            "pos": "حرف جر",
            "frequency": 20215999,
        },
        {
            "token": "المدرسة",
            "lemma": "مَدْرَسَةٌ",
            "lemma_id": 202002620,
            "root": "د ر س",
            "pos": "اسم",
            "frequency": 561184,
        },
    ]


def test_analyze_empty():
    assert morph_analyzer.analyze("") == []


def test_analyze_single_tasks():
    base_dict = {"token": "المدرسة", "frequency": 561184}
    assert morph_analyzer.analyze("المدرسة", task="pos") == [base_dict | {"pos": "اسم"}]
    assert morph_analyzer.analyze("المدرسة", task="root") == [
        base_dict | {"root": "د ر س"}
    ]
    assert morph_analyzer.analyze("المدرسة", task="lemmatization") == [
        base_dict | {"lemma": "مَدْرَسَةٌ", "lemma_id": 202002620}
    ]


@pytest.mark.parametrize(
    "word, expected",
    [
        ("الولد", True),
        ("إلى", True),
        ("école", False),
        ("123", False),
        ("", False),
    ],
)
def test_is_ar(word, expected):
    assert morph_analyzer._is_ar(word) == expected
