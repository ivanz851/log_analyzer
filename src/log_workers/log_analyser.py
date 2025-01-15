from datetime import datetime, date
from collections import Counter

from src.table import Table


class LogAnalyser:
    """
    Класс для анализа логов и получения различных статистик по данным логов.
    """

    LOCALHOST_IP = "127.0.0.1"

    @staticmethod
    def get_requests_quantity(logs: Table) -> int:
        """
        Возвращает число записей в таблице логов.

        :param logs: Таблица с данными логов.
        :return: Число записей в таблице.
        """
        return logs.size

    @staticmethod
    def get_the_most_popular_resources(logs: Table, quantity: int, request: str = "GET") -> Table:
        """
       Возвращает самые популярные ресурсы из логов, отфильтрованных по типу запроса.

       :param logs: Таблица логов.
       :param quantity: Число популярных ресурсов для вывода.
       :param request: Тип запроса, по которому происходит фильтрация.
       :return: Таблица с популярными ресурсами и их числами.
       """
        sorted_logs = [
            log["request"] for log in logs.rows
            if log.get("request_type") == request
        ]
        resource_counts = Counter(sorted_logs)
        sorted_resources = resource_counts.most_common(quantity)

        return Table([
            {"resource": resource, "value": str(count)}
            for resource, count in sorted_resources
        ])

    @staticmethod
    def get_the_most_popular_statuses(logs: Table, quantity: int) -> Table:
        """
        Возвращает самые популярные статусы ответов из логов.

        :param logs: Таблица логов.
        :param quantity: Число статусов для вывода.
        :return: Таблица с популярными статусами и их числами.
        """
        sorted_logs = [
            log["status"] for log in logs.rows
            if log.get("status") is not None
        ]
        status_counts = Counter(sorted_logs)
        sorted_statuses = status_counts.most_common(quantity)

        return Table([
            {"status": status, "responses": str(count)}
            for status, count in sorted_statuses
        ])

    @staticmethod
    def get_average_response_size(logs: Table) -> float:
        """
        Возвращает средний размер ответа (body_bytes_sent).

        :param logs: Таблица логов.
        :return: Средний размер ответа.
        """
        body_bytes_sent = [
            float(log["body_bytes_sent"]) for log in logs.rows
            if log.get("body_bytes_sent") is not None
        ]
        return sum(body_bytes_sent) / len(body_bytes_sent) if body_bytes_sent else 0.0

    @staticmethod
    def get_the_most_high_loaded_days(logs: Table, quantity: int) -> Table:
        """
        Возвращает дни с наибольшей нагрузкой по количеству запросов.

        :param logs: Таблица логов.
        :param quantity: Число дней для вывода.
        :return: Таблица с днями и числами запросов.
        """
        sorted_logs = [
            datetime.strptime(log["time_local"], "%d/%b/%Y:%H:%M:%S %z").date()
            for log in logs.rows if log.get("time_local") is not None
        ]
        day_counts = Counter(sorted_logs)
        sorted_days = day_counts.most_common(quantity)

        return Table([
            {"day": str(day), "requests": str(count)}
            for day, count in sorted_days
        ])

    @staticmethod
    def get_the_most_active_users(logs: Table, quantity: int) -> Table:
        """
        Возвращает самых активных пользователей по числу запросов.

        :param logs: Таблица логов.
        :param quantity: Число пользователей для вывода.
        :return: Таблица с IP-адресами пользователей и числами запросов.
        """
        sorted_logs = [
            log["remote_addr"] if log["remote_addr"] != "localhost" else LogAnalyser.LOCALHOST_IP
            for log in logs.rows if log.get("remote_addr") is not None
        ]
        user_counts = Counter(sorted_logs)
        sorted_users = user_counts.most_common(quantity)

        return Table([
            {"user_ip": user_ip, "requests": str(count)}
            for user_ip, count in sorted_users
        ])

    @staticmethod
    def get_date_constrained_logs(logs: Table,
                                  start_date: date | None = None,
                                  finish_date: date | None = None) -> Table:
        """
        Получает логи между двумя заданными датами (крайние даты учитываются).

        :param logs: Таблица логов.
        :param start_date: Начальная дата.
        :param finish_date: Конечная дата.
        :return: Таблица логов, удовлетворяющая ограничениям по датам.
        """
        constrained_logs = logs
        if start_date is not None:
            constrained_logs = LogAnalyser.set_from_date_constraint(constrained_logs, start_date)
        if finish_date is not None:
            constrained_logs = LogAnalyser.set_to_date_constraint(constrained_logs, finish_date)
        return constrained_logs

    @staticmethod
    def set_from_date_constraint(logs: Table, start_date: date) -> Table:
        """
        Применяет ограничение по начальной дате (включительно).

        :param logs: Таблица логов.
        :param start_date: Начальная дата.
        :return: Таблица с логами начиная с указанной даты.
        """
        return Table([
            log for log in logs.rows
            if log.get("time_local") is not None and
            datetime.strptime(log["time_local"], "%d/%b/%Y:%H:%M:%S %z").date() >= start_date
        ])

    @staticmethod
    def set_to_date_constraint(logs: Table, finish_date: date) -> Table:
        """
        Применяет ограничение по конечной дате (включительно).

        :param logs: Таблица логов.
        :param finish_date: Конечная дата для.
        :return: Таблица с логами до указанной даты.
        """
        return Table([
            log for log in logs.rows
            if log.get("time_local") is not None and
            datetime.strptime(log["time_local"], "%d/%b/%Y:%H:%M:%S %z").date() <= finish_date
        ])
