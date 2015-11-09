import os
from collections import OrderedDict

from sqlalchemy import func, select
from flask import current_app


def angular_templates():
    partials_dir = os.path.join(current_app.static_folder, 'html', 'angular')
    for (root, dirs, files) in os.walk(partials_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as fh:
                file_name = file_path[len(partials_dir) + 1:]
                yield (file_name, fh.read().decode('utf-8'))


class QueryPager(object):

    def __init__(self, engine, q):
        self.engine = engine
        self.q = q

    def limit(self, n):
        q = self.q.limit(n)
        return QueryPager(self.engine, q)

    def offset(self, n):
        q = self.q.offset(n)
        return QueryPager(self.engine, q)

    def __len__(self):
        rp = self.engine.execute(self.q.alias('counted').count())
        return rp.scalar()

    def __iter__(self):
        rp = self.engine.execute(self.q)
        while True:
            rows = rp.fetchmany(2000)
            if not rows:
                return
            for row in rows:
                yield OrderedDict(row.items())
