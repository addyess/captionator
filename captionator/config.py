from pathlib import Path
from configparser import ConfigParser


class Config:
    @classmethod
    def get(cls):
        config_file = Path("captionator.ini")
        if config_file.is_file():
            return cls(config_file)

        config_file = Path("/etc/captionator/captionator.ini")
        if config_file.is_file():
            return cls(config_file)

        return None

    def __init__(self, file_path):
        self._reader = ConfigParser()
        self._reader.read(file_path)

    def __str__(self):
        host = self.mysql_host
        user = self.mysql_user
        return f"mysql:({host}/{user})"

    @property
    def http_port(self):
        return self._reader["DEFAULT"]["port"]

    @property
    def mysql_host(self):
        return self._reader["mysql"]["host"]

    @property
    def mysql_user(self):
        return self._reader["mysql"]["user"]

    @property
    def mysql_pass(self):
        return self._reader["mysql"]["pass"]

    @property
    def google_keydir(self):
        return self._reader["google"]["keydir"]
