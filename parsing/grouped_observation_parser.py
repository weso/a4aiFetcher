from application.a4aiFetcher.parsing.parser import Parser

__author__ = 'Miguel'


class GroupedObservationParser(Parser):

    def __init__(self, log, config):
        super(GroupedObservationParser, self).__init__(log, config)

    def run(self):
        self._log.info("Running grouped observation parser")
        self._log.info("Finished parsing grouped observations")