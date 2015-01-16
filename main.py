import logging
import ConfigParser
from application.parser import Parser

__author__ = 'Miguel'


def configure_log():
    _format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename="a4aiFetcher.log", level=logging.INFO,
                        format=_format)


def run():
    configure_log()
    log = logging.getLogger("a4aiFetcher")
    config = ConfigParser.RawConfigParser()
    config.read("configuration.ini")
    parser = Parser(log, config)
    parser.run()


if __name__ == "__main__":
    run()