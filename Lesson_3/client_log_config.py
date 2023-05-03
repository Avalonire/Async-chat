import logging

logging.basicConfig(
    filename='logs/module.log',
    level=logging.DEBUG,
    format="%(asctime)s: %(levelname)s <%(module)s> -- %(message)s"
)

log = logging.getLogger('client')

# formatter = logging.Formatter(
#     "%(asctime)s: %(levelname)s <%(module)s> -- %(message)s"
# )
# fh = logging.FileHandler('logs/module.log')
# fh.setFormatter(formatter)
#
# log.addHandler(fh)
