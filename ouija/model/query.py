from copy import deepcopy
from collections import OrderedDict

from sqlalchemy import func, select


class OuijaQueryException(Exception):

    def __init__(self, query, message):
        self.query = query
        self.message = message


class OuijaQuery(object):

    def __init__(self, db, query):
        self.db = db
        self.query = query

    def clone(self):
        return OuijaQuery(self.db, deepcopy(self.query))

    def limit(self, n):
        cq = self.clone()
        cq.query['limit'] = n
        return cq

    def offset(self, n):
        cq = self.clone()
        cq.query['offset'] = n
        return cq

    def fail(self, message):
        raise OuijaQueryException(self.query, message)

    def sqla_query(self, count_only=False):
        tables = []
        columns = []
        for coldef in self.query.get('columns', []):
            table_name = coldef.get('table')
            # TODO: authz?
            table = self.db.get(table_name)
            if table is None:
                self.fail('No such table: %r' % table_name)
            tables.append(table.table)
            column_name = coldef.get('column')
            if column_name is None:
                for column in table.columns:
                    columns.append(column.column)
            else:
                column = table.get(column_name)
                if column is None:
                    self.fail('No such column: %r' % column_name)
                # TODO: support grouping
                # TODO: support sorts
                # TODO: support aggregation functions
                columns.append(column)

        if count_only:
            columns = [func.count()]
        if not len(tables):
            self.fail('No tables in query!')
        q = select(columns=columns, from_obj=tables)
        if 'limit' in self.query:
            q = q.limit(self.query.get('limit'))
        if 'offset' in self.query:
            q = q.offset(self.query.get('offset'))
        return q

    def __len__(self):
        if not hasattr(self, '_count'):
            rp = self.db.engine.execute(self.sqla_query(count_only=True))
            self._count = rp.scalar()
        return self._count

    def __iter__(self):
        rp = self.db.engine.execute(self.sqla_query())
        while True:
            rows = rp.fetchmany(2000)
            if not rows:
                return
            for row in rows:
                yield OrderedDict(row.items())
