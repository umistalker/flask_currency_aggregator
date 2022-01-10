import unittest
import models
import programm
from programm import db, cbr_api, cryptonator
import nbrb_api


class Test(unittest.TestCase):
    def setUp(self):
        models.init_db()

    def test_ndrb(self):
        xrate = db.session.query(models.XRate).filter_by().first()
        # updated_before = xrate.updated
        # self.assertEqual(xrate.rate, 1.0)
        nbrb_api.Api().update_rate(840, 975)
        xrate = db.session.query(models.XRate).filter_by(id=1).first()
        # updated_after = xrate.updated
        print(xrate.rate)
        self.assertGreater(xrate.rate, 2.5)
        # self.assertGreater(updated_after, updated_before)
        api_log = db.session.query(models.ApiLog).filter_by(id=1).first()
        self.assertIsNotNone(api_log)
        self.assertEqual(api_log.request_url, 'https://www.nbrb.by/api/exrates/rates?periodicity=0')
        db.session.remove()

    def test_cbr(self):
        xrate = db.session.query(models.XRate).filter_by(id=2).first()
        # updated_before = xrate.updated
        # self.assertEqual(xrate.rate, 1.0)
        cbr_api.Api().update_rate(840, 13)
        xrate = db.session.query(models.XRate).filter_by(id=2).first()
        # updated_after = xrate.updated
        print(xrate.rate)
        self.assertGreater(xrate.rate, 60)
        api_log = db.session.query(models.ApiLog).filter_by(id=1).first()
        self.assertIsNotNone(api_log)
        self.assertEqual(api_log.request_url, 'http://www.cbr.ru/scripts/XML_daily.asp')
        db.session.remove()

    # def test_api_error(self):
    #     config.Config.HTTP_TIMEOUT = 0.001
    #     xrate = db.session.query(models.XRate).filter_by(id=1).first()
    #     self.assertRaises(requests.exceptions.RequestException, nbrb_api.Api().update_rate, 840, 980)
    #     api_log = db.session.query(models.ApiLog).filter_by(id=1).first()
    #     self.assertIsNotNone(api_log)
    #     api_log = db.session.query(models.ApiLog).filter_by(id=1).first()
    #     error_log = db.session.query(models.ErrorLog).filter_by(id=1).first()
    #     self.assertIsNone(error_log)
    #     self.assertIsNotNone(error_log.traceback)
    #     self.assertEqual(api_log.error, error_log.traceback)
    #     config.Config.HTTP_TIMEOUT = 15

    def test_cypt(self):
        from_currency=1000
        to_currency=643
        xrate = db.session.query(models.XRate).filter_by(id=3).first()
        cryptonator.Api().update_rate(from_currency=from_currency, to_currency=to_currency)
        xrate = db.session.query(models.XRate).filter_by(id=3).first()
        self.assertGreater(xrate.rate, 10000)
        api_log = db.session.query(models.ApiLog).filter_by(id=1).first()

        self.assertIsNotNone(api_log)
        db.session.remove()

if __name__ == '__main__':
    unittest.main()
