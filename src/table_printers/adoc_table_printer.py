import logging

from src.table_printers.table_printer import TablePrinter

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class AdocTablePrinter(TablePrinter):
    """
    Класс для печати таблиц в формате AsciiDoc.

    Данный класс реализует методы для вывода таблиц с выравниванием текста в ячейках и отображением
    заданного числа строк.
    """

    @staticmethod
    def print_table(table, lines_quantity: int, header: str = "") -> None:
        """
        Печатает таблицу с заголовком и заданным числом строк.

        :param table: Таблица с данными.
        :param lines_quantity: Число строк для печати.
        :param header: Заголовок таблицы, который будет напечатан перед таблицей (по умолчанию пустая строка).
        """
        if header:
            LOGGER.info(f"= {header}")

        LOGGER.info("|===")

        AdocTablePrinter.print_column_names(table)
        AdocTablePrinter.print_table_rows(table, lines_quantity)

        LOGGER.info("|===")

    @staticmethod
    def print_column_names(table) -> None:
        """
        Печатает названия столбцов таблицы.

        :param table: Таблица с данными.
        """
        columns = table.columns
        column_lengths = table.get_columns_lengths()

        header_row = "".join(
            f"|{AdocTablePrinter.center_text(column, column_lengths[column])}"
            for column in columns
        )
        LOGGER.info(header_row)
        LOGGER.info("")

    @staticmethod
    def print_table_rows(table, num_of_rows_to_print: int) -> None:
        """
        Печатает строки таблицы.

        :param table: Таблица с данными.
        :param num_of_rows_to_print: Число строк для печати.
        """
        columns = table.columns
        column_lengths = table.get_columns_lengths()

        for line in range(min(num_of_rows_to_print, table.size)):
            row_parts = []

            for column in columns:
                cell_value = table.get_cell(line, column) or table.DEFAULT_CELL_VALUE
                centered_text = AdocTablePrinter.center_text(cell_value, column_lengths[column])
                row_parts.append(f"|{centered_text} ")

            row = "".join(row_parts)
            LOGGER.info(row)
