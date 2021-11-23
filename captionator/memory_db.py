from collections import defaultdict
from uuid import uuid4


class MemDB:
    _storage = defaultdict(dict)

    def _get(self, table, allowed_columns, views=None, filters=None):
        if not views or not all(v.lower() in allowed_columns for v in views):
            views = list(allowed_columns)
        rows = self._storage[table]
        return views, [
            [
                rid if v == 'id' else row.get(v)
                for v in views
            ]
            for rid, row in rows.items()
            if filters is None or all(
                (rid if k == 'id' else row.get(v)) == v
                for k, v in filters.items()
            )
        ]

    def _delete(self, table, rid):
        self._storage[table].pop(rid)

    def _set(self, table, rid, **settable):
        for k, v in settable.items():
            if k != 'id':
                self._storage[table][rid][k] = v

    def _create(self, table, **settable):
        row_id = len(self._storage[table])
        self._storage[table][row_id] = settable
        return row_id
