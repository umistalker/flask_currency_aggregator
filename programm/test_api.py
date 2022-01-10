import logging

import config
from models import db, XRate

log = logging.getLogger('TestApi')
fh = logging.FileHandler((config.Config.LOGGER_CONFIG['file']))
fh.setFormatter((config.Config.LOGGER_CONFIG['formatter']))
log.addHandler(fh)
log.setLevel((config.Config.LOGGER_CONFIG['level']))


def update_xrates(from_currency, to_currency):
    log.info("Started update for: %s=>%s" % (from_currency, to_currency))
    try:
        xrate = db.session.query(XRate).filter_by(to_currency=to_currency, from_currency=from_currency).first()
    except AttributeError:
        return {"message": "Attribute Error"}, 500
    log.debug('Rate before %s', xrate)
    xrate.rate += 0.01
    db.session.add(xrate)
    db.session.commit()
    log.debug(f"Rate after: %s", xrate)
    log.info('Finish update for: %s=>%s' % (from_currency, to_currency))
