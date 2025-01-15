import itertools


class Table:
    """
    Класс Table релизует таблицу с данными, в которой каждая строка хранится в виде словаря стобцов.
    В таблице могут быть разные столбцы в разных строках..
    """
    DEFAULT_CELL_VALUE = "None"

    def __init__(self, rows: list[dict[str, str | None]]):
        """
        Инициализирует таблицу с переданными строками.

        :param rows: Список строк, где каждая строка представлена как словарь с именами столбцов и значениями.
        :raises ValueError: Если список строк пуст.
        """

        if not rows:
            raise ValueError("Rows cannot be empty")

        self._rows = rows
        keys = list(set().union(itertools.chain.from_iterable(rows)))
        self.columns = list(keys)

    @property
    def rows(self) -> list[dict[str, str | None]]:
        """
        Возвращает строки таблицы.

        :return: Список строк, каждая из которых представлена как словарь.
        """
        return self._rows

    @property
    def size(self) -> int:
        """
        Возвращает число строк в таблице.

        :return: Число строк.
        """
        return len(self._rows)

    def add_rows(self, new_rows: list[dict[str, str]]) -> None:
        """
        Добавляет заданные строки в таблицу.

        :param new_rows: Список строк для добавления, каждая строка представлена словарем столбцов.
        """
        self._rows.extend(new_rows)
        new_columns = {key for row in new_rows for key in row}
        self.columns = list(set(self.columns).union(new_columns))

    def add_row(self, new_row: dict[str, str]) -> None:
        """
        Добавляет одну заданную строку в таблицу.

        :param new_row: Новая строка, представленная словарем столбцов.
        """
        self._rows.append(new_row)
        new_columns = set(new_row.keys())
        self.columns = list(set(self.columns).union(new_columns))

    def get_columns_lengths(self) -> dict[str, int]:
        """
        Возвращает длины всех столбцов тоблицы. Длина столбца — максимальная длина значения
        в этом столбце по всем строкам (или длина названия столбца, если она больше).

        :return: Словарь, в котором ключи — названия столбцов, значения — длины столбцов.
        """
        return {column: self.get_column_length(column) for column in self.columns}

    def get_column_length(self, column: str) -> int:
        """
        Для заданного столбца возвращает максимальную длину значений по всем строкам.

        :param column: Название столбца, длину которого ищем.
        :raises ValueError: Если столбца нет в таблице.
        :return: Максимальная длина значений в столбце.
        """
        if column not in self.columns:
            raise ValueError("No such column")

        max_length = max(
            (len(row.get(column, self.DEFAULT_CELL_VALUE))
             for row in self._rows),
            default=0
        )
        return max(max_length, len(column))

    def get_cell(self, row_ind: int, column: str) -> str | None:
        """
        Возвращает значение в ячейке таблицы по заданной строке и столбцу.

        :param row_ind: Индекс строки.
        :param column: Название столбца.
        :return: Значение в ячейке (DEFAULT_CELL_VALUE, если значение отсутствует).
        """
        return self._rows[row_ind].get(column, self.DEFAULT_CELL_VALUE)
