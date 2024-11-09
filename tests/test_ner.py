from sinatools.ner.entity_extractor import extract


def test_extract_entities_nested():
    assert extract("ذهب محمد إلى جامعة بيرزيت", ner_method="nested") == [
        {"token": "ذهب", "tags": "O"},
        {"token": "محمد", "tags": "B-PERS"},
        {"token": "إلى", "tags": "O"},
        {"token": "جامعة", "tags": "B-ORG"},
        {"token": "بيرزيت", "tags": "B-GPE I-ORG"},
    ]


def test_extract_entities_flat():
    assert extract("ذهب محمد إلى جامعة بيرزيت", ner_method="flat") == [
        {"token": "ذهب", "tags": "O"},
        {"token": "محمد", "tags": "B-PERS"},
        {"token": "إلى", "tags": "O"},
        {"token": "جامعة", "tags": "B-ORG"},
        {"token": "بيرزيت", "tags": "I-ORG"},
    ]
