from ouija.core import url_for
from ouija.model.util import normalize_column_type


class OuijaDatabase(object):

    def __init__(self, engine, meta, config):
        self.engine = engine
        self.meta = meta
        self.config = config

    @property
    def tables(self):
        if not hasattr(self, '_tables'):
            self._tables = []
            for table in self.meta.tables.values():
                table = OuijaTable(self, table)
                self._tables.append(table)
        return self._tables

    def by_name(self, table_name):
        for table in self.tables:
            if table.name == table_name:
                return table


class OuijaTable(object):

    def __init__(self, database, table):
        self.database = database
        self.table = table

    @property
    def name(self):
        return self.table.name

    @property
    def config(self):
        return self.database.config.get('tables', {}).get(self.name, {})

    @property
    def label(self):
        return self.config.get('label', self.name)

    @property
    def roles(self):
        return set(self.config.get('roles', []))

    @property
    def columns(self):
        if not hasattr(self, '_columns'):
            self._columns = []
            for column in self.table.columns:
                self._columns.append(OuijaColumn(self, column))
        return self._columns

    def to_dict(self):
        return {
            'name': self.name,
            'label': self.label,
            'metadata_uri': url_for('tables.view', table_name=self.name),
            'rows_uri': url_for('tables.rows', table_name=self.name),
            'columns_num': len(self.columns),
            'rows_num': 0,  # len(QueryPager(engine, q))
            'columns': self.columns
        }


class OuijaColumn(object):

    def __init__(self, table, column):
        self.table = table
        self.column = column

    @property
    def name(self):
        return self.column.name

    @property
    def config(self):
        return self.table.config.get('columns', {}).get(self.name, {})

    @property
    def label(self):
        return self.config.get('label', self.name)

    @property
    def type(self):
        return normalize_column_type(self.column)

    def to_dict(self):
        return {
            'name': self.name,
            'label': self.label,
            'type': self.type,
            'numeric': self.type in ['integer', 'float']
        }
