import logging
import traceback
from datetime import datetime

import requests

from config import Config
from programm import db
from programm.models import XRate, ApiLog, ErrorLog

fh = logging.FileHandler((Config.LOGGER_CONFIG['file']))
fh.setFormatter((Config.LOGGER_CONFIG['formatter']))
fh.setLevel((Config.LOGGER_CONFIG['level']))


class _Api:
    def __init__(self, logger_name):
        self.log = logging.getLogger(logger_name)
        self.log.addHandler(fh)
        self.log.setLevel(Config.LOGGER_CONFIG['level'])

    def update_rate(self, from_currency, to_currency):
        self.log.info("Started update for: %s=>%s" % (from_currency, to_currency))
        try:
            xrate = db.session.query(XRate).filter_by(to_currency=to_currency, from_currency=from_currency).first()
        except AttributeError:
            return {"message": "Attribute Error"}, 500
        self.log.debug('Rate before %s', xrate)
        xrate.rate = self._update_rate(xrate)
        db.session.add(xrate)
        db.session.commit()
        self.log.debug(f"Rate after: %s", xrate)
        self.log.info('Finish update for: %s=>%s' % (from_currency, to_currency))

    def _update_rate(self, xrate):
        raise NotImplementedError('_update_rate')

    def _send_request(self, url, method, data=None, headers=None):
        log = ApiLog(request_url=url, request_data=data, request_method=method, request_headers=headers)
        try:
            response = self._send(method=method, url=url, headers=headers, data=data)
            log.response_text = response.text
            return response
        except Exception as ex:
            self.log.exception("Error during request sending")
            log.error = str(ex)
            error = ErrorLog(
                        request_data=data,
                        request_url=url,
                        request_method=method,
                        error=str(ex),
                        traceback=traceback.format_exc(chain=False))
            db.session.add(error)
            db.session.commit()
            raise
        finally:
            db.session.add(log)
            db.session.commit()

    def _send(self, url, method, data=None, headers=None):
        return requests.request(method=method, url=url, headers=headers, data=data, timeout=Config.HTTP_TIMEOUT)