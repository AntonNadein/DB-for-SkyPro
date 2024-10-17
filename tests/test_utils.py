import unittest
from unittest.mock import patch

import pytest

from src.utils import create_list, selection_condition


class TestSelectionCondition(unittest.TestCase):
    """Тест функции логики выбора"""

    @patch("builtins.input", side_effect=["1", "2", "3", "4", "5", "0"])
    def test_selection_condition(self, mock_input):
        result = selection_condition("question", "1", "2", "3", "4", "5")
        self.assertEqual(result, "1")

        result = selection_condition("question", "1", "2", "3")
        self.assertEqual(result, "2")

        result = selection_condition("question", "1", "2", "3", "4")
        self.assertEqual(result, "3")

        result = selection_condition("question", "1", "2", "3", "4")
        self.assertEqual(result, "4")

        result = selection_condition("question", "1", "2", "3", "4", "5")
        self.assertEqual(result, "5")

        result = selection_condition("question", "1", "2")
        self.assertEqual(result, "exit")


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("1, 2", (["1", "2"])),
        ("2,1", (["2", "1"])),
        ("", ("")),
        ("Текст без запятых", ("Текст без запятых")),
    ],
)
def test_create_list(input_data, expected):
    """Тест функции получения списка из стоки"""
    assert create_list(input_data) == expected
