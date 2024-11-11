# TODO: Fix the import error in Github Actions
"""
______________________ ERROR collecting tests/test_ner.py ______________________
tests/test_ner.py:1: in <module>
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

try:
    from sinatools.ner.entity_extractor import extract
except Exception as e:
    print(e)


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
