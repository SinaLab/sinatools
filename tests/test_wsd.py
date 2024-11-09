import pytest

from sinatools.wsd.disambiguator import disambiguate


@pytest.mark.skip(
    reason="TODO: fails with error "
    "`RuntimeError: Could not infer dtype of numpy.int64`. "
    "TODO 2: datasets not available by default in download_files."
)
def test_disambiguate():
    assert disambiguate("تمشيت بين الجداول والأنهار") == [
        {"concept_id": "303051631", "word": "تمشيت", "lemma": "تَمَشَّى"},
        {"concept_id": "303005470", "word": "بين", "lemma": "بَيْن"},
        {"concept_id": "303007335", "word": "الجداول", "lemma": "جَدْوَلٌ"},
        {"concept_id": "303056588", "word": "والأنهار", "lemma": "نَهْرٌ"},
    ]


@pytest.mark.skip(
    reason="TODO: fails with error "
    "`RuntimeError: Could not infer dtype of numpy.int64`. "
    "TODO 2: datasets not available by default in download_files."
)
def test_disambiguate_2():
    assert disambiguate(
        "أعلنت وزارة المالية في فلسطين"
        " عن تخفيض ضريبة الدخل في الضفة الغربية وقطاع غزة"
    ) == [
        {"concept_id": "303037486", "word": "أعلنت", "lemma": "أَعْلَنَ"},
        {"word": "وزارة المالية", "gloss": "اسم مؤسسة"},
        {"concept_id": "202000985", "word": "في", "lemma": "فِي2"},
        {"word": "فلسطين", "gloss": "اسم بلد، له حدود إدارية/جيوسياسية"},
        {"concept_id": "303037863", "word": "عن", "lemma": "عَنْ"},
        {"concept_id": "303015224", "word": "تخفيض", "lemma": "تَخْفِيضٌ"},
        {"concept_id": "333001533", "word": "ضريبة الدخل", "lemma": "ضريبة الدخل"},
        {"concept_id": "202000985", "word": "في", "lemma": "فِي2"},
        {"word": "الضفة الغربية", "gloss": "اسم بلد، له حدود إدارية/جيوسياسية"},
        {"word": "وقطاع غزة", "gloss": "اسم بلد، له حدود إدارية/جيوسياسية"},
    ]
