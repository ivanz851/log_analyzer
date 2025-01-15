import unittest
from src.table import Table


class TestTableWithNginxLogs(unittest.TestCase):

    def setUp(self):
        self.nginx_logs = [
            {
                "remote_addr": "192.168.1.1",
                "remote_user": "-",
                "time_local": "10/Oct/2023:13:55:36 +0000",
                "request": "GET /index.html HTTP/1.1",
                "status": "200",
                "body_bytes_sent": "1024",
                "http_referer": "-",
                "http_user_agent": "Mozilla/5.0"
            },
            {
                "remote_addr": "192.168.1.2",
                "remote_user": "user1",
                "time_local": "10/Oct/2023:13:56:01 +0000",
                "request": "POST /submit-form HTTP/1.1",
                "status": "404",
                "body_bytes_sent": "512",
                "http_referer": "http://example.com",
                "http_user_agent": "Mozilla/5.0"
            }
        ]
        self.table = Table(self.nginx_logs)

    def test_initialization(self):
        self.assertEqual(self.table.size, 2, "Таблица должна содержать 2 строки после инициализации")
        self.assertIn("remote_addr", self.table.columns, "В таблице должен быть столбец 'remote_addr'")
        self.assertIn("status", self.table.columns, "В таблице должен быть столбец 'status'")
        self.assertIn("http_user_agent", self.table.columns, "В таблице должен быть столбец 'http_user_agent'")

        self.assertNotIn("nonexistent_column", self.table.columns,
                         "В таблице не должно быть столбца 'nonexistent_column'")

    def test_add_row_with_nginx_format(self):
        new_log = {
            "remote_addr": "192.168.1.3",
            "remote_user": "-",
            "time_local": "10/Oct/2023:14:00:00 +0000",
            "request": "GET /about HTTP/1.1",
            "status": "200",
            "body_bytes_sent": "2048",
            "http_referer": "http://example.com/about",
            "http_user_agent": "Mozilla/5.0"
        }
        self.table.add_row(new_log)
        self.assertEqual(self.table.size, 3, "Таблица должна содержать 3 строки после добавления новой строки")
        self.assertEqual(self.table.get_cell(2, "remote_addr"),
                         "192.168.1.3",
                         "Значение 'remote_addr' в новой строке должно быть '192.168.1.3'")

    def test_get_columns_lengths_for_nginx_fields(self):
        lengths = self.table.get_columns_lengths()
        self.assertEqual(lengths["remote_addr"],
                         max(len("remote_addr"), len("192.168.1.2")),
                         "Длина столбца 'remote_addr' должна соответствовать максимальной длине IP адреса")
        self.assertEqual(lengths["request"],
                         max(len("request"), len("POST /submit-form HTTP/1.1")),
                         "Длина столбца 'request' должна соответствовать самой длинной команде запроса")
        self.assertEqual(lengths["status"], len("status"),
                         "Длина столбца 'status' должна соответствовать длине кода статуса")

    def test_get_cell_for_nginx_log(self):
        self.assertEqual(self.table.get_cell(0, "status"),
                         "200",
                         "Ячейка (0, 'status') должна содержать '200'")
        self.assertEqual(self.table.get_cell(1, "http_referer"),
                         "http://example.com",
                         "Ячейка (1, 'http_referer') должна содержать 'http://example.com'")
        self.assertEqual(self.table.get_cell(1, "body_bytes_sent"),
                         "512",
                         "Ячейка (1, 'body_bytes_sent') должна содержать '512'")

    def test_get_cell_with_missing_value(self):
        self.assertEqual(self.table.get_cell(0, "http_referer"), "-",
                         "Если 'http_referer' отсутствует, оно должно быть '-'")
        self.assertEqual(self.table.get_cell(0, "nonexistent_column"), "None",
                         "Если столбец не существует, должно вернуться значение по умолчанию 'None'")
