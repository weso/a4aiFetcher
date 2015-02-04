from application.a4aiFetcher.parsing.excel_model.excel_observation import ExcelObservation
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
        data_file_name = self._config.get("DATA_ACCESS", "FILE_NAME")
        primary_sheet_number = self._config.getint("PRIMARY_OBSERVATIONS", "SHEET_NUMBER")
        primary_obs_sheet = self.get_sheet(data_file_name, primary_sheet_number)
        return primary_obs_sheet

    def retrieve_primary_observations(self, primary_obs_sheet):
        country_column = self._config.getint("PRIMARY_OBSERVATIONS", "COUNTRY_COLUMN")
        country_start_row = self._config.getint("PRIMARY_OBSERVATIONS", "COUNTRY_START_ROW")
        indicator_codes_row = self._config.getint("PRIMARY_OBSERVATIONS", "INDICATOR_CODES_ROW")
        indicator_start_column = self._config.getint("PRIMARY_OBSERVATIONS", "INDICATOR_START_COLUMN")

        for row_number in range(country_start_row, primary_obs_sheet.nrows):
            for column_number in range(indicator_start_column, primary_obs_sheet.ncols):
                country_name = primary_obs_sheet.cell(row_number, country_column).value
                indicator_code = primary_obs_sheet.cell(indicator_codes_row, column_number).value
                observation_value = primary_obs_sheet.cell(row_number, column_number).value
                observation = ExcelObservation(country_name, indicator_code, observation_value)
                self._excel_primary_observations.append(observation)
                print observation.country_name + " " + observation.indicator_code + " " + str(observation.value)

    def store_primary_observations(self):
        pass

    def rank_observations_by_type(self):
        pass