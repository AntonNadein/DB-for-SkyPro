from unittest.mock import patch

import pytest
from requests.exceptions import RequestException, Timeout

from src.class_get_API import HeadHunterAPI, ParserHH


def test_hh_api():
    """тест экземпляров класса HeadHunterAPI"""
    hh_api = HeadHunterAPI("Python")
    assert hh_api.search_text == "Python"
    assert hh_api.params == {"page": 0, "per_page": 30, "text": "Python"}


@patch("requests.get")
def test_get_api_hh(mocked_get):
    """тест работы HeadHunterAPI"""
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = {"items": [{"id": "test1"}, {"id": "test2"}]}
    hh_api = HeadHunterAPI("Python")
    result_1 = hh_api.get_vacancies_from_employer_id()
    result_2 = hh_api.get_employer_list_id
    assert result_1 == [{"id": "test1"}, {"id": "test2"}, {"id": "test1"}, {"id": "test2"}]
    assert result_2 == ["test1", "test2"]


def test_request_exception(parser_hh):
    """Тест ошибки: общие ошибки запроса"""
    with patch("requests.get", side_effect=RequestException):
        with pytest.raises(RequestException):
            print(parser_hh.get_vacancies)


@patch("requests.get")
def test_failed_response(mocked_get, parser_hh, test_list_dict_input, capsys):
    """Тест ошибки: сайт не отвечает"""
    mocked_get.return_value.status_code = 404
    mocked_get.return_value.json.return_value = test_list_dict_input
    result = parser_hh.get_vacancies
    message = capsys.readouterr()
    assert message.out.strip().split("\n")[0] == "Запрос не был успешным."
    assert message.out.strip().split("\n")[-1] == "Произошла ошибка."
    assert result is None


def test_timeout_exception(parser_hh):
    """Тест ошибки: время ожидания превышино"""
    with patch("requests.get", side_effect=Timeout):
        with pytest.raises(Timeout):
            print(parser_hh.get_vacancies)


def test_parser_hh_init():
    """Тест ошибки: время ожидания превышино"""
    with pytest.raises(TypeError):
        ParserHH(123)
