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


def parse(log, config):
    indicator_parser = IndicatorParser(log, config)
    secondary_observation_parser = SecondaryObservationParser(log, config)
    primary_observation_parser = PrimaryObservationParser(log, config)
    grouped_observation_parser = GroupedObservationParser(log, config)
    ranker = Ranker(log, config)
    enricher = Enricher(log, config)

    indicator_parser.run()
    secondary_observation_parser.run()
    primary_observation_parser.run()
    grouped_observation_parser.run()
    ranker.run()
    enricher.run()


if __name__ == "__main__":
    run()
    print "Done! :)"