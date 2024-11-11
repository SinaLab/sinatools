import pytest

from sinatools.synonyms.synonyms_generator import evaluate_synonyms, extend_synonyms


@pytest.mark.skip(reason="TODO: fix. Verify datasets and models.")
def test_extend_synonyms():
    # TODO: fix. It returns `[['مسلك', 0.5], ['camber', 0.5]]`
    assert extend_synonyms("ممر | طريق", level=2) == [
        ["مَسْلَك", "61%"],
        ["سبيل", "61%"],
        ["وَجْه", "30%"],
        ["نَهْج", "30%"],
        ["نَمَطٌ", "30%"],
        ["مِنْهَج", "30%"],
        ["مِنهاج", "30%"],
        ["مَوْر", "30%"],
        ["مَسَار", "30%"],
        ["مَرصَد", "30%"],
        ["مَذْهَبٌ", "30%"],
        ["مَدْرَج", "30%"],
        ["مَجَاز", "30%"],
    ]


@pytest.mark.skip(reason="TODO: fix. Verify datasets and models.")
def test_evaluate_synonyms():
    # TODO: fix. It returns `[['مَسْلَك', 0], ['ممر', 0], ['طريق', 0], ['سبيل', 0]]`
    assert evaluate_synonyms("ممر | طريق | مَسْلَك | سبيل", level=2) == [
        ["مَسْلَك", "61%"],
        ["سبيل", "60%"],
        ["طريق", "40%"],
        ["ممر", "40%"],
    ]
