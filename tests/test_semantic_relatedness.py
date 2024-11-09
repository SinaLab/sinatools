import pytest

from sinatools.semantic_relatedness.compute_relatedness import get_similarity_score


def test_get_similarity_score():
    sentence1 = "تبلغ سرعة دوران الأرض حول الشمس حوالي 110 كيلومتر في الساعة."
    sentence2 = "تدور الأرض حول محورها بسرعة تصل تقريبا 1670 كيلومتر في الساعة."
    assert get_similarity_score(sentence1, sentence2) == pytest.approx(0.9, 0.1)
