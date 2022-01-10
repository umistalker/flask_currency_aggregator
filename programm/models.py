import datetime
import decimal
from sqlalchemy import create_engine
from inspect import stack, getframeinfo
import config
from programm import db


class XRate(db.Model):
    __tablename__ = 'xrate'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    from_currency = db.Column(db.Integer)
    to_currency = db.Column(db.Integer)
    rate = db.Column(db.Float)
    updated = db.Column(db.Date, default=datetime.datetime.now())

    def __init__(self, from_currency, to_currency, rate):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.rate = rate

    def __repr__(self):
        return f'XRate({self.from_currency}, {self.to_currency},{self.rate},{self.updated})'


class ApiLog(db.Model):
    __tablename__ = 'api_logs'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    request_url = db.Column(db.String)
    request_data = db.Column(db.Text, nullable=True)
    request_method = db.Column(db.String)
    request_headers = db.Column(db.Text, nullable=True)
    response_text = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime)
    finished = db.Column(db.DateTime)
    error = db.Column(db.Text, nullable=True)
    module = db.Column(db.Text)

    def __init__(self, request_url, request_data, request_method, request_headers, response_text=None,
                 error=None):
        self.request_url = request_url
        if not request_data:
            self.request_data = []
        else:
            self.request_data = request_data
        self.request_data = request_data
        if not request_headers:
            self.request_method = []
        else:
            self.request_method = request_method
        if not response_text:
            self.response_text = []
        else:
            self.request_headers = request_headers
        self.response_text = response_text
        self.created = datetime.datetime.now()
        self.finished = datetime.datetime.now()
        if not error:
            self.error = []
        else:
            self.error = error
        self.module = str(getframeinfo(stack()[0][0]).filename)
    def __repr__(self):
        return f'Errors({self.error}, {self.request_url},{self.created},{self.finished})'


class ErrorLog(db.Model):
    __tablename__ = 'error_logs'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    request_url = db.Column(db.String)
    request_data = db.Column(db.Text, nullable=True)
    request_method = db.Column(db.String)
    created = db.Column(db.DateTime)
    error = db.Column(db.Text, nullable=True)
    traceback = db.Column(db.Text, nullable=True)

    def __init__(self, request_url, request_data, request_method, traceback,
                 error):
        self.request_url = request_url
        self.request_data = request_data
        self.request_method = request_method
        self.created = datetime.datetime.now()
        self.traceback = traceback
        self.error = error

    def __repr__(self):
        return f'Errors_Log({self.error}, {self.request_url},{self.created}, {self.traceback})'


def init_db():
    print("Delete all rows")
    engine = create_engine(config.Config.SQLALCHEMY_DATABASE_URI)

    try:
        XRate.__table__.drop(engine)
        ApiLog.__table__.drop(engine)
        ErrorLog.__table__.drop(engine)
    except:
        pass

    try:
        XRate.__table__.create(engine)
        ApiLog.__table__.create(engine)
        ErrorLog.__table__.create(engine)

    # try:
    #     XRate.query.delete_cascade()
    #     ApiLog.query.delete_cascade()
    except:
        pass

    print("Create new rows")
    new_rate1 = XRate(
        from_currency=840,
        to_currency=975,
        rate=1.0
    )
    new_rate2 = XRate(
        from_currency=840,
        to_currency=13,
        rate=1.0
    )
    new_rate3 = XRate(
        from_currency=1000,
        to_currency=643,
        rate=1.0
    )
    db.session.add(new_rate1)
    db.session.commit()
    db.session.add(new_rate2)
    db.session.commit()
    db.session.add(new_rate3)
    db.session.commit()
    print("Done")

