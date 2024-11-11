import pytest

# TODO: Fix the import error in Github Actions
"""
___________________ ERROR collecting tests/test_relations.py ___________________
tests/test_relations.py:3: in <module>
    from sinatools.relations.relation_extractor import event_argument_relation_extraction
sinatools/relations/relation_extractor.py:2: in <module>
    from sinatools.ner.entity_extractor import extract
sinatools/ner/__init__.py:22: in <module>
    tag_vocab = pickle.load(fh)
/opt/hostedtoolcache/Python/3.12.7/x64/lib/python3.12/site-packages/torchtext/__init__.py:18: in <module>
    from torchtext import _extension  # noqa: F401
/opt/hostedtoolcache/Python/3.12.7/x64/lib/python3.12/site-packages/torchtext/_extension.py:64: in <module>
    _init_extension()
/opt/hostedtoolcache/Python/3.12.7/x64/lib/python3.12/site-packages/torchtext/_extension.py:58: in _init_extension
    _load_lib("libtorchtext")
/opt/hostedtoolcache/Python/3.12.7/x64/lib/python3.12/site-packages/torchtext/_extension.py:50: in _load_lib
    torch.ops.load_library(path)
/opt/hostedtoolcache/Python/3.12.7/x64/lib/python3.12/site-packages/torch/_ops.py:1350: in load_library
    ctypes.CDLL(path)
/opt/hostedtoolcache/Python/3.12.7/x64/lib/python3.12/ctypes/__init__.py:379: in __init__
    self._handle = _dlopen(self._name, mode)
E   OSError: /opt/hostedtoolcache/Python/3.12.7/x64/lib/python3.12/site-packages/torchtext/lib/libtorchtext.so: undefined symbol: _ZN5torch3jit17parseSchemaOrNameERKSs
"""


@pytest.mark.skip(
    reason="Fails with error: `RuntimeError: Numpy is not available`. "
    "Apparently, it needs numpy<2."
)
def test_event_argument_relation_extraction():
    try:
        from sinatools.relations.relation_extractor import (
            event_argument_relation_extraction,
        )
    except Exception as e:
        print(e)
        return
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
