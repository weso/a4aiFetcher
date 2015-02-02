from application.a4aiFetcher.parsing.parser import Parser

__author__ = 'Miguel'


class PrimaryObservationParser(Parser):

    def __init__(self, log, config):
        super(PrimaryObservationParser, self).__init__(log, config)

    def run(self):
        self._log.info("Running primary observation parser")
        self._log.info("Finished parsing primary observations")