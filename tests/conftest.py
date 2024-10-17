import pytest

from src.class_get_API import ParserHH


@pytest.fixture
def test_list_dict_input():
    return {"items": [{"name": "test1", "area": {"name": "test3"}, "salary": "test2", "alternate_url": "test4"}]}


@pytest.fixture
def parser_hh():
    return ParserHH("Юрист")
