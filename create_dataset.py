"""PowerBI Dataset Encoder

This module allows the user to easily create a dataset that can be pushed to a PowerBI workspace

Classes are created to represent Rows, Columns, Tables, and Datasets:
- Tables are made up of Rows and Columns
- Datasets are made up of Tables

"""

class Dataset:
    """
    A class to represent a dataset.
    Stores the table object and dataset attributes
    """

    def __init__(self, name: str, default_mode="Push", tables=None):
        self.name = name
        self.default_mode = default_mode
        self.tables = tables

    def __repr__(self):
        return f'<Dataset {str(self.__dict__)}>'


class DatasetEncoder:
    """
    A class to represent a dataset encoder.
    Converts table object and datset attributes into a dictionary
    """
    def encode(self, dataset: Dataset):
        table_encoder = TableEncoder()

        json_data = {
            "name": dataset.name,
            "defaultMode": dataset.default_mode, 
            "tables": [table_encoder.encode(x) for x in dataset.tables],
        }

        return json_data


class Table:
    """
    A class to represent a table.
    Stores the column and row objects
    """
    def __init__(self, name: str, columns: list, rows=None):
        self.name = name
        self.columns = columns
        self.rows = rows

    def __repr__(self):
        return f'<Table {str(self.__dict__)}>'


class TableEncoder:
    """
    A class to represent a table encoder.
    Converts row and column attributes of table object into a dictionary
    """
    def encode(self, table: Table):
        json_data = {
            "name": table.name,
        }

        if table.columns is not None:
            column_encoder = ColumnEncoder()
            json_data["columns"] = [column_encoder.encode(x) for x in table.columns]

        if table.rows is not None:
            row_encoder = RowEncoder()
            json_data["rows"] = [row_encoder.encode(x) for x in table.rows]

        return json_data


class Column:
    """
    A class to represent a column.
    Stores the column name and column data type
    """
    def __init__(self, name: str, data_type: str):
        self.name = name
        self.data_type = data_type

    def __repr__(self):
        return f'<Column {str(self.__dict__)}>'


class ColumnEncoder:
    """
    A class to represent a column encoder.
    Converts attributes of column object into a dictionary
    """
    def encode(self, column: Column):
        json_data = {
            "name": column.name,
            "dataType": column.data_type
        }

        return json_data


class Row:
    """
    A class to represent a row.
    Stores the column name and row value as an attribute
    """
    def __init__(self, row_data: dict):
        for key in row_data:
            setattr(self, key, row_data[key])

    def __repr__(self):
        return f'<Row {str(self.__dict__)}>'

class RowEncoder:
    """
    A class to represent a row encoder.
    Converts instance attribute into a dictionary
    """
    def encode(self, row: Row):
        return row.__dict__