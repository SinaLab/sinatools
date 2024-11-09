import pytest

from sinatools.utils import parser, word_compare


class TestParser:
    @pytest.mark.parametrize(
        "input_text, expected_output, kwargs",
        [
            ("2023الجو جميلُ", "الجو جميل", {}),
            ("جَمِيلُ", "جَمِيلُ", {"diacs": False}),
            ("إِيمَان", "إيمان", {"alif": False}),
            ("أبريل?! 2024", "أبريل 2024", {"alif": False, "digit": False}),
        ],
    )
    def test_ar_strip(self, input_text, expected_output, kwargs):
        assert parser.arStrip(input_text, **kwargs) == expected_output

    # TODO: remove_latin keeps spaces. Check if this is the expected behavior.
    @pytest.mark.parametrize(
        "input_text, expected_output",
        [
            ("miojkdujhvaj1546545spkdpoqfoiehwv", " 1546545 "),
            (
                "أصل المسمى «تخطيط موارد المؤسسة» هو Enterprise Resource Planning",
                "أصل المسمى «تخطيط موارد المؤسسة» هو      ",
            ),
        ],
    )
    def test_remove_latin(self, input_text, expected_output):
        assert parser.remove_latin(input_text) == expected_output

    @pytest.mark.parametrize(
        "input_text, expected_output",
        [
            ("te!@#،$%%؟st", "test"),
            ("{يَا أَيُّهَا الَّذِينَ آمَنُوا لِيَسْتَأْذِنْكُمُ....}", "يَا أَيُّهَا الَّذِينَ آمَنُوا لِيَسْتَأْذِنْكُمُ"),
        ],
    )
    def test_remove_punctuation(self, input_text, expected_output):
        assert parser.remove_punctuation(input_text) == expected_output


class TestWordCompare:
    def test_implication(self):
        implication = word_compare.Implication("ذهب", "ذهب")
        assert implication.get_verdict() == "Same"
        assert implication.get_conflicts() == 0
        assert implication.get_distance() == 0

        # # TODO: Fix this test. Should return "Same" instead of "Different".
        assert word_compare.Implication("ذَهَب", "ذهب").get_verdict() == "Same"
    
