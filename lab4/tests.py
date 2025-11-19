import pytest
from lib.tasks import circle_areas_generator, email_generator, filter_string
import math
import re


class TestCircleAreasGenerator:
    def test_first_value(self):
        gen = circle_areas_generator()
        first_area = next(gen)
        expected = math.pi * (10 ** 2)
        assert first_area == pytest.approx(expected)

    def test_generator_length(self):
        gen = circle_areas_generator()
        count = sum(1 for _ in gen)
        assert count == 91

    def test_values_range(self):
        gen = circle_areas_generator()
        for radius, area in zip(range(10, 101), gen):
            expected = math.pi * (radius ** 2)
            assert area == pytest.approx(expected)

    def test_last_value(self):
        gen = circle_areas_generator()
        areas = list(gen)
        last_area = areas[-1]
        expected = math.pi * (100 ** 2)
        assert last_area == pytest.approx(expected)

class TestEmailGenerator:
    def test_email_format(self):
        gen = email_generator()
        email = next(gen)
        assert '@mail.ru' in email
        assert email.endswith('@mail.ru')
        local_part = email.split('@')[0]
        assert len(local_part) == 8

    def test_email_local_part_chars(self):
        gen = email_generator()
        email = next(gen)
        local_part = email.split('@')[0]
        allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
        for char in local_part:
            assert char in allowed_chars

    def test_multiple_emails_unique(self):
        gen = email_generator()
        emails = [next(gen) for _ in range(10)]
        assert len(emails) == len(set(emails))

    def test_email_generator_infinite(self):
        gen = email_generator()
        for _ in range(100):
            email = next(gen)
            assert isinstance(email, str)
            assert len(email) == 8 + len("@mail.ru")

    def test_email_regex_pattern(self):
        gen = email_generator()
        email = next(gen)
        pattern = r'^[a-zA-Z0-9_]{8}@mail\.ru$'
        assert re.match(pattern, email) is not None


class TestFilterString:
    def test_normal_case(self):
        result = filter_string("8 15 345 42 -5 100 67 9 88")
        assert result == [15, 42, 67, 88]

    def test_empty_input(self):
        result = filter_string("")
        assert result == []

    def test_only_spaces(self):
        result = filter_string("   ")
        assert result == []

    def test_no_two_digit_numbers(self):
        result = filter_string("1 2 3 100 999")
        assert result == []

    def test_boundary_values(self):
        result = filter_string("9 10 99 100")
        assert result == [10, 99]

    def test_negative_numbers(self):
        result = filter_string("-10 -99 15 -42 99")
        assert result == [-10, -99, 15, -42, 99]

    def test_invalid_input(self):
        with pytest.raises(ValueError):
            filter_string("abc 42 def")

    def test_whitespace_handling(self):
        result = filter_string("  15   42   67  ")
        assert result == [15, 42, 67]

    def test_single_two_digit_number(self):
        result = filter_string("42")
        assert result == [42]

    def test_single_non_two_digit_number(self):
        result = filter_string("5")
        assert result == []

    def test_large_numbers(self):
        result = filter_string("999 1000 50 1234 99")
        assert result == [50, 99]

    def test_zero_and_single_digit(self):
        result = filter_string("0 1 2 3 4 5 6 7 8 9")
        assert result == []

    def test_mixed_valid_invalid(self):
        with pytest.raises(ValueError):
            filter_string("10 20 abc 30")

    def test_negative_boundary(self):
        result = filter_string("-9 -10 -99 -100")
        assert result == [-10, -99]

    def test_only_three_digit_numbers(self):
        result = filter_string("100 200 300 999")
        assert result == []

    def test_very_large_input(self):
        numbers = " ".join(str(i) for i in range(-1000, 1001))
        result = filter_string(numbers)
        for num in result:
            assert (10 <= abs(num) <= 99)
        expected_count = (99 - 10 + 1) * 2  # положительные и отрицательные
        assert len(result) == expected_count


if __name__ == "__main__":
    pytest.main([__file__, "-v"])