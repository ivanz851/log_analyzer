import unittest
from src.log_workers.log_parser import LogParser
from src.table import Table


class TestLogParser(unittest.TestCase):

    def setUp(self):
        self.valid_log = (
            '127.0.0.1 - - [08/Nov/2024:10:52:20 +0000] '
            '"GET /index.html HTTP/1.1" 200 1024 '
            '"https://example.com" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"'
        )

        self.invalid_log = 'Некорректная строка лога'

    def test_parse_log_valid(self):
        parsed_log = LogParser.parse_log(self.valid_log)
        expected_data = {
            "remote_addr": "127.0.0.1",
            "remote_user": "-",
            "time_local": "08/Nov/2024:10:52:20 +0000",
            "request_type": "GET",
            "request": "/index.html",
            "protocol": "HTTP/1.1",
            "status": "200",
            "body_bytes_sent": "1024",
            "http_referer": "https://example.com",
            "http_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        self.assertEqual(parsed_log, expected_data, "Лог должен парситься корректно")

    def test_parse_log_invalid(self):
        parsed_log = LogParser.parse_log(self.invalid_log)
        self.assertIsNone(parsed_log, "Некорректная строка лога должна возвращать None")

    def test_parse_logs(self):
        logs = [self.valid_log, self.invalid_log]
        parsed_table = LogParser.parse_logs(logs)
        self.assertIsInstance(parsed_table, Table, "Метод parse_logs должен возвращать объект Table")
        self.assertEqual(parsed_table.size, 1, "Таблица должна содержать только корректно разобранные логи")

    def test_column_names(self):
        self.assertIn("remote_addr", LogParser.column_names, "Должен присутствовать столбец 'remote_addr'")
        self.assertIn("status", LogParser.column_names, "Должен присутствовать столбец 'status'")
        self.assertEqual(len(LogParser.column_names), 10, "Должно быть ровно 10 столбцов в column_names")
