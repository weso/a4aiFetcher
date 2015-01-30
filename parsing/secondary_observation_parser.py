from application.a4aiFetcher.parsing.parser import Parser

__author__ = 'Miguel'


class SecondaryObservationParser(Parser):

    def __init__(self, log, config):
        super(SecondaryObservationParser, self).__init__(log, config)

    def run(self):
        self._log.info("Running secondary observation parser")
        self._log.info("Finished parsing secondary observations")