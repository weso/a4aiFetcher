import logging
import ConfigParser
from application.a4aiFetcher.enrichment.enricher import Enricher
from application.a4aiFetcher.parsing.grouped_observation_parser import GroupedObservationParser
from application.a4aiFetcher.parsing.indicator_parser import IndicatorParser
from application.a4aiFetcher.parsing.primary_observation_parser import PrimaryObservationParser
from application.a4aiFetcher.parsing.ranker import Ranker
from application.a4aiFetcher.parsing.secondary_observation_parser import SecondaryObservationParser

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
    parse(log, config)
    rank(log, config)
    enrich(log, config)


def parse(log, config):
    IndicatorParser(log, config).run()
    SecondaryObservationParser(log, config).run()
    PrimaryObservationParser(log, config).run()
    GroupedObservationParser(log, config).run()


def rank(log, config):
    ranker = Ranker(log, config)
    ranker.run()


def enrich(log, config):
    enricher = Enricher(log, config)
    enricher.run()

if __name__ == "__main__":
    run()
    print "Done! :)"