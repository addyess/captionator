import mysql.connector
import mysql.connector.errors

from collections import OrderedDict

from captionator.memory_db import MemDB


class DBAccessError(Exception):
    """Custom Error for DB Errors"""


class DB:
    schema = OrderedDict(
        id="INT NOT NULL AUTO_INCREMENT PRIMARY KEY",
        name="VARCHAR(255)",
        text="TEXT",
        location="Undefined",
    )

    def __init__(self, config):
        self._config = config
        self._mydb, self._memdb = None, None
        try:
            self._mydb = mysql.connector.connect(
                host=self._config.mysql_host,
                user=self._config.mysql_user,
                password=self._config.mysql_pass,
                database="captionator",
            )
            self._mydb.autocommit = True
        except mysql.connector.errors.DatabaseError:
            self._memdb = MemDB()

    def captions(self, **kwargs):
        allowed_columns = self.schema.keys()
        returned_columns, fetched = self._get("captions", allowed_columns, **kwargs)
        return [{returned_columns[i]: v for i, v in enumerate(r)} for r in fetched]

    def create_captions(self, values):
        valid_to_set = set(self.schema.keys()) - {"id"}
        settable = {k: values.get(k) for k in valid_to_set if values.get(k)}
        if settable:
            return self._create("captions", **settable)
        raise ValueError("No settable values available")

    def set_captions(self, rid, values):
        valid_to_set = set(self.schema.keys()) - {"id"}
        settable = {k: values.get(k) for k in valid_to_set if values.get(k)}
        if settable:
            self._set("captions", rid, **settable)

    def del_captions(self, rid):
        self._delete("captions", rid)

    def _get(self, table, allowed_columns, views=None, filters=None):
        if self._mydb:
            select, where = "*", ""
            if views and all(v.lower() in allowed_columns for v in views):
                select = ", ".join(views)
            else:
                views = list(allowed_columns)
            if filters and all(f.lower() in allowed_columns for f in filters):
                where = " WHERE " + " AND ".join(f"{col} = %({col})s" for col in filters)
            cursor = self._mydb.cursor()
            statement = f"SELECT {select} FROM {table}{where}"
            cursor.execute(statement, params=filters)
            return views, cursor.fetchall()
        if self._memdb:
            return self._memdb._get(table, allowed_columns, views=views, filters=filters)

    def _delete(self, table, rid):
        if self._mydb:
            cursor = self._mydb.cursor()
            where = {"id": rid}
            cursor.execute(f"DELETE from {table} where id = %(id)s", where)
        elif self._memdb:
            return self._memdb._delete(table, rid)

    def _set(self, table, rid, **settable):
        if self._mydb:
            settable["id"] = rid
            settings = "SET " + ", ".join(f"{col} = %({col})s" for col in settable)
            cursor = self._mydb.cursor()
            cursor.execute(f"UPDATE {table} {settings} where id = %(id)s", settable)
        elif self._memdb:
            self._memdb._set(table, rid, **settable)

    def _create(self, table, **settable):
        if self._mydb:
            keys, values = zip(*settable.items())
            keys_str = ", ".join(keys)
            value_str = ", ".join("%s" for col in values)
            cursor = self._mydb.cursor()
            insert_stmt = f"INSERT INTO {table} ({keys_str}) VALUES ({value_str})"
            cursor.execute(insert_stmt, values)
            return cursor.lastrowid
        elif self._memdb:
            return self._memdb._create(table, **settable)