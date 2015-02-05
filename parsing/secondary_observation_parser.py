from application.a4aiFetcher.parsing.parser import Parser

__author__ = 'Miguel'


class SecondaryObservationParser(Parser):

    def __init__(self, log, config):
        super(SecondaryObservationParser, self).__init__(log, config)

    def run(self):
        self._log.info("Running secondary observation parser")
        secondary_obs_sheet = self.initialize_secondary_obs_sheet()
        self.retrieve_secondary_observations(secondary_obs_sheet)
        self.store_secondary_observations()
        self._log.info("Finished parsing secondary observations")

    def initialize_secondary_obs_sheet(self):
        pass

    def retrieve_secondary_observations(self, secondary_obs_sheet):
        pass

    def store_secondary_observations(self):
        pass