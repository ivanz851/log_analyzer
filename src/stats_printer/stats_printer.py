from datetime import date

from src.log_workers.log_analyser import LogAnalyser
from src.table import Table


class StatsPrinter:
    """
    Класс для отображения статистики из логов.
    """

    def __init__(self, table_printer):
        """
        Инициализирует StatsPrinter с заданным форматом вывода таблиц.
        """
        self.table_printer = table_printer

    def print_overall_info(
            self, logs: Table, sources: list[str], from_date: date | None, to_date: date | None
    ) -> None:
        """
        Печатает общую информацию по логам: число файлов, диапазон дат, число запросов,
        средний размер ответа.

        :param logs: Таблица логов.
        :param sources: Список путей к файлам или URL с логами.
        :param from_date: Начальная дата фильтрации логов, если указана.
        :param to_date: Конечная дата фильтрации логов, если указана.
        """
        table = Table([
            {"metrics": "Files", "value": str(sources)},
            {"metrics": "Start date", "value": str(from_date)},
            {"metrics": "End date", "value": str(to_date)},
            {"metrics": "Requests", "value": str(LogAnalyser.get_requests_quantity(logs))},
            {"metrics": "Average response size", "value": str(LogAnalyser.get_average_response_size(logs))}
        ])
        self.table_printer.print_table(table, table.size, header="Overall information")

    def print_most_popular_resources(self, logs: Table, lines_in_table: int) -> None:
        """
        Печатает самые популярные ресурсы, отсортированные по частоте запросов.

        :param logs: Таблица логов.
        :param lines_in_table: Число строк для отображения в таблице.
        """
        resources = LogAnalyser.get_the_most_popular_resources(logs, lines_in_table)
        self.table_printer.print_table(resources, header="The most popular resources")

    def print_most_popular_statuses(self, logs: Table, lines_quantity: int) -> None:
        """
        Печатает самые популярные коды статусов, отсортированные по частоте встречаемости.

        :param logs: Таблица логов.
        :param lines_quantity: Число строк для отображения в таблице.
        """
        statuses = LogAnalyser.get_the_most_popular_statuses(logs, lines_quantity)
        self.table_printer.print_table(statuses, lines_quantity=lines_quantity, header="The most popular statuses")

    def print_most_high_loaded_days(self, logs: Table, lines_quantity: int) -> None:
        """
        Печатает дни с наибольшей загрузкой по числу запросов.

        :param logs: Таблица логов.
        :param lines_quantity: Число строк для отображения в таблице.
        """
        days = LogAnalyser.get_the_most_high_loaded_days(logs, lines_quantity)
        self.table_printer.print_table(days, lines_quantity=lines_quantity, header="The most highloaded days")

    def print_most_active_users(self, logs: Table, lines_quantity: int) -> None:
        """
        Печатает наиболее активных пользователей, отсортированных по количеству запросов.

        :param logs: Таблица логов.
        :param lines_quantity: Число строк для отображения в таблице.
        """
        users = LogAnalyser.get_the_most_active_users(logs, lines_quantity)
        self.table_printer.print_table(users, lines_quantity=lines_quantity, header="The most active users")
