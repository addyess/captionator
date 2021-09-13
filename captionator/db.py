import mysql.connector
from collections import namedtuple, OrderedDict


class DB:
    schema = OrderedDict(
        id="INT NOT NULL AUTO_INCREMENT PRIMARY KEY",
        name="VARCHAR(255)",
        text="TEXT",
        location="Undefined"
    )

    def __init__(self, config):
        self._config = config
        self._mydb = mysql.connector.connect(
            host=self._config.mysql_host,
            user=self._config.mysql_user,
            password=self._config.mysql_pass,
            database="captionator"
        )
        self._mydb.autocommit = True

    def captions(self, **kwargs):
        allowed_columns = self.schema.keys()
        returned_columns, fetched = self._get('captions', allowed_columns, **kwargs)
        return [
            {returned_columns[i]: v for i, v in enumerate(r)}
            for r in fetched
        ]

    def set_captions(self, rid, values):
        valid_to_set = set(self.schema.keys()) - {"id"}
        settable = {k: values.get(k) for k in valid_to_set if values.get(k)}
        if settable:
            self._set("captions", rid, **settable)

    def _get(self, table, allowed_columns, views=None, filters=None):
        select, where = "*", ""
        if views and all(v.lower() in allowed_columns for v in views):
            select = ", ".join(views)
        else:
            views = list(allowed_columns)
        if filters and all(f.lower() in allowed_columns for f in filters):
            where = " WHERE " + " AND ".join(
                f"{col} = %({col})s"
                for col in filters
            )
        cursor = self._mydb.cursor()
        statement = f"SELECT {select} FROM {table}{where}"
        cursor.execute(statement, params=filters)
        return views, cursor.fetchall()

    def _set(self, table, rid, **settable):
        settings = "SET " + ", ".join(f"{col} = %({col})s" for col in settable)
        cursor = self._mydb.cursor()
        cursor.execute(f"UPDATE {table} {settings} where id = {rid}", settable)
