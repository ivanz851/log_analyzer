import re

from src.table import Table


class LogParser:
    """
    Класс для парсинга логов и создания таблицы с данными из них.
    """
    column_names = [
        "remote_addr",
        "remote_user",
        "time_local",
        "request_type",
        "request",
        "protocol",
        "status",
        "body_bytes_sent",
        "http_referer",
        "http_user_agent"
    ]

    date_time_regex = r"\d{2}/[A-Z][a-z]{2}/\d{4}:\d{2}:\d{2}:\d{2} [\-\+]\d{4}"
    log_regex = re.compile(
        r"(\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}) - "    # remote_addr
        r"([^ ]+) "                                   # remote_user
        r"\[(" + date_time_regex + r")] "             # time_local
        r"\"(\w+) "                                   # request_type 
        r"(/[^ ]*) "                                  # request
        r"(HTTP/.+)\" "                               # protocol
        r"(\d+) "                                     # status
        r"(\d+) "                                     # body_bytes_sent
        r"\"(.+)\" "                                  # http_referer 
        r"\"(.+)\""                                   # http_user_agent
    )

    @staticmethod
    def parse_logs(logs: list[str]) -> Table:
        """
        Парсит несколько строк логов и преобразует их в таблицу.

        :param logs: Список строк логов для парсинга.
        :return: Таблица с преобразованными данными.
        """
        return Table([LogParser.parse_log(log) for log in logs if LogParser.parse_log(log) is not None])

    @staticmethod
    def parse_log(log: str) -> dict[str, str | None] | None:
        """
        Парсит одну строку лога в словарь, в котором ключи - это имена столбцов, а значения - данные из строки лога.

        :param log: Строка лога для парсинга.
        :return: Словарь с данными или None, если лог не соответствует ожидаемому формату.
        """
        if not LogParser.log_regex.match(log):
            return None

        captured_groups = LogParser.log_regex.match(log).groups()
        parsed_log = {LogParser.column_names[i]: captured_groups[i] for i in range(0, len(captured_groups))}

        return parsed_log

    @staticmethod
    def combine_logs(sources: list[str]) -> list[str]:
        """
        Считывает логи из нескольких источников (локальные файлы или URL).

        :param sources: Список путей к локальным файлам или URL.
        :return: Список строк, содержащий все логи.
        """
        logs_data = []

        for src in sources:
            url_regex = r"(?:http)s?://.*"

            if re.match(url_regex, src):
                import requests
                response = requests.get(src)
                logs_data.extend(response.text.splitlines())
            else:
                with open(src, 'r') as file:
                    logs_data.extend(file.readlines())

        return logs_data
