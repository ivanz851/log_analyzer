import logging

from src.table import Table
from src.table_printers.table_printer import TablePrinter

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class MarkdownTablePrinter(TablePrinter):
    """
    Класс для печати таблиц в формате Markdown.

    Данный класс реализует методы для вывода таблиц с выравниванием текста в ячейках и отображением
    заданного числа строк.
    """

    @staticmethod
    def print_table(table: Table, lines_quantity: int, header: str = "") -> None:
        """
        Печатает таблицу в формате Markdown с заданным числом строк и заголовком.

        :param table: Таблица с данными.
        :param lines_quantity: Число строк для печати.
        :param header: Заголовок таблицы.
        """
        if header:
            LOGGER.info(f"#### {header}")

        MarkdownTablePrinter.print_column_names(table)
        MarkdownTablePrinter.print_head_separator(table)
        MarkdownTablePrinter.print_table_rows(table, lines_quantity)

    @staticmethod
    def print_column_names(table: Table) -> None:
        """
        Печатает названия столбцов таблицы.

        :param table: Таблица с данными.
        """
        columns = table.columns
        column_lengths = table.get_columns_lengths()

        header_row = "|" + "|".join(
            MarkdownTablePrinter.center_text(column, column_lengths[column])
            for column in columns
        ) + "|"
        LOGGER.info(header_row)

    @staticmethod
    def print_head_separator(table: Table) -> None:
        """
        Печатает разделитель под заголовком таблицы.

        :param table: Таблица с данными.
        """
        column_lengths = table.get_columns_lengths()

        separator_row = "|" + "|".join(
            f":{'-' * (length - 2)}:"
            for length in column_lengths.values()
        ) + "|"
        LOGGER.info(separator_row)

    @staticmethod
    def print_table_rows(table: Table, num_of_rows_to_print: int) -> None:
        """
        Печатает строки таблицы.

        :param table: Таблица с данными.
        :param num_of_rows_to_print: Число строк для печати.
        """
        column_lengths = table.get_columns_lengths()
        columns = table.columns

        for line in range(min(num_of_rows_to_print, table.size)):
            row = "|" + "|".join(
                MarkdownTablePrinter.center_text(table.get_cell(line, column) or "null", column_lengths[column])
                for column in columns
            ) + "|"
            LOGGER.info(row)
