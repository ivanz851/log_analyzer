import unittest
from datetime import date
from src.table import Table
from src.log_workers.log_analyser import LogAnalyser


class TestLogAnalyser(unittest.TestCase):

    def setUp(self):
        self.logs = Table([
            {
                "remote_addr": "192.168.1.1",
                "remote_user": "-",
                "time_local": "08/Nov/2024:10:52:20 +0000",
                "request_type": "GET",
                "request": "/index.html",
                "protocol": "HTTP/1.1",
                "status": "200",
                "body_bytes_sent": "1024",
                "http_referer": "https://example.com",
                "http_user_agent": "Mozilla/5.0"
            },
            {
                "remote_addr": "192.168.1.2",
                "remote_user": "-",
                "time_local": "08/Nov/2024:11:00:00 +0000",
                "request_type": "POST",
                "request": "/form_submit",
                "protocol": "HTTP/1.1",
                "status": "404",
                "body_bytes_sent": "2048",
                "http_referer": "-",
                "http_user_agent": "Mozilla/5.0"
            },
            {
                "remote_addr": "127.0.0.1",
                "remote_user": "-",
                "time_local": "09/Nov/2024:15:30:00 +0000",
                "request_type": "GET",
                "request": "/about",
                "protocol": "HTTP/1.1",
                "status": "200",
                "body_bytes_sent": "512",
                "http_referer": "-",
                "http_user_agent": "curl/7.68.0"
            }
        ])

    def test_get_requests_quantity(self):
        quantity = LogAnalyser.get_requests_quantity(self.logs)
        self.assertEqual(quantity, 3, "Должно быть 3 записи в таблице логов")

    def test_get_the_most_popular_resources(self):
        popular_resources = LogAnalyser.get_the_most_popular_resources(self.logs, 2)
        self.assertEqual(popular_resources.size, 2, "Должно быть 2 популярных ресурса в таблице")
        self.assertEqual(popular_resources.rows[0]["resource"], "/index.html",
                         "Самый популярный ресурс должен быть '/index.html'")

    def test_get_the_most_popular_statuses(self):
        popular_statuses = LogAnalyser.get_the_most_popular_statuses(self.logs, 2)
        self.assertEqual(popular_statuses.size, 2, "Должно быть 2 популярных статуса в таблице")
        self.assertEqual(popular_statuses.rows[0]["status"], "200", "Самый популярный статус должен быть '200'")

    def test_get_average_response_size(self):
        avg_size = LogAnalyser.get_average_response_size(self.logs)
        correct_avg_size = 1194.66666667
        EPS = 1e-8

        self.assertLess(abs(avg_size - correct_avg_size),
                         EPS,
                         f"Средний размер ответа должен быть {correct_avg_size} байт")

    def test_get_the_most_high_loaded_days(self):
        popular_days = LogAnalyser.get_the_most_high_loaded_days(self.logs, 2)
        self.assertEqual(popular_days.size, 2, "Должно быть 2 дня с самой высокой нагрузкой")
        self.assertEqual(popular_days.rows[0]["day"], "2024-11-08", "Самый нагруженный день должен быть '2024-11-08'")

    def test_get_the_most_active_users(self):
        active_users = LogAnalyser.get_the_most_active_users(self.logs, 2)
        self.assertEqual(active_users.size, 2, "Должно быть 2 активных пользователя")
        self.assertEqual(active_users.rows[0]["user_ip"], "192.168.1.1",
                         "Самый активный пользователь должен быть с IP '192.168.1.1'")

    def test_get_date_constrained_logs(self):
        start_date = date(2024, 11, 8)
        finish_date = date(2024, 11, 8)
        constrained_logs = LogAnalyser.get_date_constrained_logs(self.logs, start_date, finish_date)
        self.assertEqual(constrained_logs.size, 2, "Должно быть 2 лога между 08/Nov/2024 и 08/Nov/2024 включительно")

    def test_set_from_date_constraint(self):
        start_date = date(2024, 11, 9)
        constrained_logs = LogAnalyser.set_from_date_constraint(self.logs, start_date)
        self.assertEqual(constrained_logs.size, 1, "Должен быть только 1 лог начиная с 09/Nov/2024")

    def test_set_to_date_constraint(self):
        finish_date = date(2024, 11, 8)
        constrained_logs = LogAnalyser.set_to_date_constraint(self.logs, finish_date)
        self.assertEqual(constrained_logs.size, 2, "Должно быть 2 лога до 08/Nov/2024 включительно")
