import logging
import logging.handlers as lh

logging.basicConfig(
    filename='logs/module.log',
    level=logging.DEBUG,
    format="%(asctime)s: %(levelname)s <%(name)s> -- %(message)s"
)

log = logging.getLogger('server')

# formatter = logging.Formatter(
#     "%(asctime)s: %(levelname)s <%(module)s> -- %(message)s"
# )
# fh = logging.FileHandler('logs/module.log')
# fh.setFormatter(formatter)
#
# log.addHandler(fh)

th = lh.TimedRotatingFileHandler('logs/module.log', when='D', interval=1)
log.addHandler(th)
