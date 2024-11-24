from abc import ABC, abstractmethod

from src.table import Table


class TablePrinter(ABC):
    """
    Абстрактный класс для вывода таблиц в различных форматах (markdown и adoc).
    """

    @staticmethod
    @abstractmethod
    def print_table(table: Table, lines_quantity: int, header: str = "") -> None:
        """
        Метод для печати таблицы.

        :param table: Таблицы, который содержит строки данных и метаданные.
        :param lines_quantity: Число строк для печати. По умолчанию - все строки.
        :param header: Заголовок таблицы.
        :return: None
        """
        pass

    @staticmethod
    def center_text(text: str, col_width: int) -> str:
        """
        Выравнивает по центру текст в столбце с заданной шириной.

        :param text: Текст, который нужно выровнять по центру.
        :param col_width: Ширина строки, в которой нужно выровнять текст.
        :return: Текст с добавленными пробелами по краям, выровненный по центру.
        """
        padding = max(col_width - len(text), 0)
        left_padding = padding // 2
        right_padding = padding - left_padding
        return f"{' ' * left_padding}{text}{' ' * right_padding}"
