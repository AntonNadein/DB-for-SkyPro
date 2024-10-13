from unittest.mock import patch

from src.class_db_manager import DataBase


@patch("psycopg2.connect")
@patch("os.getenv")
def test_connect_db(mock_getenv, mock_connect):
    mock_getenv.side_effect = lambda key: {
        "DATABASE_HOST": "test_host",
        "DATABASE_NAME": "test_db",
        "DATABASE_USER": "test_user",
        "DATABASE_PASSWORD": "test_password",
    }[key]

    db = DataBase()
    db.connect_data_base()
    mock_connect.assert_called_once_with(
        host="test_host", database="test_db", user="test_user", password="test_password", port=5432
    )


@patch("os.getenv")
def test_db_attributes(mock_getenv):
    mock_getenv.side_effect = lambda key: {
        "DATABASE_HOST": "test_host",
        "DATABASE_NAME": "test_db",
        "DATABASE_USER": "test_user",
        "DATABASE_PASSWORD": "test_password",
    }[key]

    db = DataBase()
    assert db.host == "test_host"
    assert db.database == "test_db"
    assert db.user == "test_user"
    assert db.password == "test_password"
    assert db.port == 5432
