from logging import basicConfig


def configure_logging(loglevel="INFO"):
    basicConfig(level=loglevel)
