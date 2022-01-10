import logging


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://mark:mark12345@localhost:5432/new_database1"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOGGER_CONFIG = dict(level=logging.DEBUG,
                         file='app.log',
                         formatter=logging.Formatter("%(asctime)s [%(levelname)s] - %(name)s^%(message)s"))

    HTTP_TIMEOUT = 15