from application.a4aiFetcher.parsing.parser import Parser

__author__ = 'Miguel'


class PrimaryObservationParser(Parser):

    def __init__(self, log, config):
        super(PrimaryObservationParser, self).__init__(log, config)
        self._excel_primary_observations = []

    def run(self):
        self._log.info("Running primary observation parser")
        primary_obs_sheet = self.initialize_primary_obs_sheet()
        self.retrieve_primary_observations(primary_obs_sheet)
        self.store_primary_observations()
        self.rank_observations_by_type()
        self._log.info("Finished parsing primary observations")

    def initialize_primary_obs_sheet(self):
        pass

    def retrieve_primary_observations(self, primary_obs_sheet):
        pass

    def store_primary_observations(self):
        pass

    def rank_observations_by_type(self):
        pass