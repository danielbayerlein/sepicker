from datetime import datetime
import pytest

from sepicker.datasinks.mysql import Mysql


class TestMysql:
    @pytest.fixture(autouse=True)
    def mock_mysql_connect(self, mocker):
        return mocker.patch('mysql.connector.connect', autospec=True)

    @pytest.fixture
    def mysql_instance(self):
        user = 'user'
        password = 'password'  # noqa: S105
        host = 'localhost'
        database = 'database'

        return Mysql(user, password, host, database)

    def test_mysql_init(self, mysql_instance):
        assert mysql_instance.user == 'user'
        assert mysql_instance.password == 'password'  # noqa: S105
        assert mysql_instance.host == 'localhost'
        assert mysql_instance.database == 'database'

    def test_enter(self, mock_mysql_connect, mysql_instance):
        client_instance = mock_mysql_connect.return_value

        with mysql_instance:
            pass

        mock_mysql_connect.assert_called_once_with(  # noqa: S106
            user='user',
            password='password',
            host='localhost',
            database='database'
        )
        assert client_instance.cursor.called

    def test_exit(self, mock_mysql_connect, mysql_instance):
        client_instance = mock_mysql_connect.return_value

        with mysql_instance:
            pass

        assert client_instance.commit.called
        assert client_instance.cursor().close.called
        assert client_instance.close.called

    def test_save(self, mock_mysql_connect, mysql_instance):
        client_instance = mock_mysql_connect.return_value
        values = [(datetime.now(), 'OUTSIDE_TEMPERATURE', '24.5')]

        with mysql_instance as mysql:
            mysql.save(values)

        client_instance. \
            cursor() \
            .executemany \
            .assert_called_once_with(
                'INSERT INTO sepicker(timestamp, name, value) '
                'VALUES(%s, %s, %s)',
                values
            )
