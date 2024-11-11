import pytest

# TODO: Fix the import error in Github Actions
"""
______________________ ERROR collecting tests/test_wsd.py ______________________
tests/test_wsd.py:3: in <module>
    from sinatools.wsd.disambiguator import disambiguate
sinatools/wsd/disambiguator.py:9: in <module>
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
    reason="TODO: fails with error "
    "`RuntimeError: Could not infer dtype of numpy.int64`. "
    "TODO 2: datasets not available by default in download_files."
)
def test_disambiguate():
    try:
        from sinatools.wsd.disambiguator import disambiguate
    except Exception as e:
        print(e)
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
    try:
        from sinatools.wsd.disambiguator import disambiguate
    except Exception as e:
        print(e)
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
