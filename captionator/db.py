import mysql.connector
from collections import namedtuple, OrderedDict

CaptionFile = namedtuple('CaptionFile', 'uuid, name, text')


class DB:
    def __init__(self, config):
        self._config = config
        print(config)
        self._mydb = mysql.connector.connect(
            host=self._config.mysql_host,
            user=self._config.mysql_user,
            password=self._config.mysql_pass,
            database="captionator"
        )
        schema = OrderedDict(
            id="INT NOT NULL AUTO_INCREMENT PRIMARY KEY",
            name="VARCHAR(255)",
            text="TEXT"
        )
        self._create_table("captions", schema)

    def captions(self, views=None, filters=None):
        allowed_columns = ['id', 'name', 'text']
        return [
            CaptionFile(*r) for r in self._get_table(allowed_columns, views, filters)
        ]

    def _get_table(self, table, allowed_columns, views=None, filters=None):
        cursor = self._mydb.cursor()
        select, where = "*", ""
        if views and all(v.lower() in allowed_columns for v in views):
            select = ",".join(views)
        if filters and all(v.lower in filters for v in views):
            where = "where " + " ".join(
                f"{col} = %({col})s'"
                for col, value in filters.items()
            )
        cursor.execute(f"SELECT {select} from captions {where}", filters)
        return cursor.fetchall()

    def _create_table(self, name, schema):
        cursor = self._mydb.cursor()
        definition = ", ".join(f"{col} {type}" for col, type in schema.items())
        try:
            cursor.execute(f"CREATE table {name} ({definition})")
        except mysql.connector.errors.ProgrammingError:
            pass
