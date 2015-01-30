from application.a4aiFetcher.parsing.parser import Parser

__author__ = 'Miguel'


class IndicatorParser(Parser):

    def __init__(self, log, config):
        super(IndicatorParser, self).__init__(log, config)

    def run(self):
        self._log.info("Running indicator parser")
        self.retrieve_indicators(self._indicator_sheet)
        self.store_indicators(self._indicator_repo)
        self._log.info("Finished parsing indicators")