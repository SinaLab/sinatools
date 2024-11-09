import pytest

from sinatools.relations.relation_extractor import event_argument_relation_extraction


@pytest.mark.skip(
    reason="Fails with error: `RuntimeError: Numpy is not available`. "
    "Apparently, it needs numpy<2."
)
def test_event_argument_relation_extraction():
    assert event_argument_relation_extraction(
        "اندلعت انتفاضة الأقصى في 28 سبتمبر 2000"
    ) == [
        {
            "TripleID": "1",
            "Subject": {"ID": 1, "Type": "EVENT", "Label": "انتفاضة الأقصى"},
            "Relation": "location",
            "Object": {"ID": 2, "Type": "FAC", "Label": "الأقصى"},
        },
        {
            "TripleID": "2",
            "Subject": {"ID": 1, "Type": "EVENT", "Label": "انتفاضة الأقصى"},
            "Relation": "happened at",
            "Object": {"ID": 3, "Type": "DATE", "Label": "28 سبتمبر 2000"},
        },
    ]
