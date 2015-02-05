from application.a4aiFetcher.parsing.excel_model.excel_observation import ExcelObservation
from application.a4aiFetcher.parsing.parser import Parser
from application.a4aiFetcher.parsing.utils import excel_observation_to_dom

__author__ = 'Miguel'


class SecondaryObservationParser(Parser):

    def __init__(self, log, config):
        super(SecondaryObservationParser, self).__init__(log, config)
        self._excel_secondary_observations = []

    def run(self):
        self._log.info("Running secondary observation parser")
        secondary_obs_sheet = self.initialize_secondary_obs_sheet()
        self.retrieve_secondary_observations(secondary_obs_sheet)
        self.store_secondary_observations()
        self._log.info("Finished parsing secondary observations")

    def initialize_secondary_obs_sheet(self):
        data_file_name = self._config.get("DATA_ACCESS", "FILE_NAME")
        secondary_sheet_number = self._config.getint("SECONDARY_OBSERVATIONS", "SHEET_NUMBER")
        secondary_obs_sheet = self.get_sheet(data_file_name, secondary_sheet_number)
        return secondary_obs_sheet

    def retrieve_secondary_observations(self, secondary_obs_sheet):
        country_column = self._config.getint("SECONDARY_OBSERVATIONS", "COUNTRY_COLUMN")
        country_start_row = self._config.getint("SECONDARY_OBSERVATIONS", "COUNTRY_START_ROW")
        indicator_codes_row = self._config.getint("SECONDARY_OBSERVATIONS", "INDICATOR_CODES_ROW")
        indicator_start_column = self._config.getint("SECONDARY_OBSERVATIONS", "INDICATOR_START_COLUMN")

        for row_number in range(country_start_row, secondary_obs_sheet.nrows):
            for column_number in range(indicator_start_column, secondary_obs_sheet.ncols):
                country_name = secondary_obs_sheet.cell(row_number, country_column).value
                indicator_code = secondary_obs_sheet.cell(indicator_codes_row, column_number).value
                observation_value = secondary_obs_sheet.cell(row_number, column_number).value
                observation = ExcelObservation(country_name, indicator_code, observation_value)
                self._excel_secondary_observations.append(observation)

    def store_secondary_observations(self):
        for excel_observation in self._excel_secondary_observations:
            area = self._area_repo.find_by_name(excel_observation.country_name)
            indicator = self._indicator_repo.find_indicators_by_code(excel_observation.indicator_code)
            observation = excel_observation_to_dom(excel_observation, area, indicator)
            observation_uri = self._config.get("OTHERS", "HOST") + "observations/" + indicator.indicator + "/" \
                              + area.iso3 + "/" + str(observation.year.value)
            self._observation_repo.insert_observation(observation, observation_uri=observation_uri,
                                                      area_iso3_code=area.iso3, indicator_code=indicator.indicator,
                                                      year_literal=str(observation.year.value), area_name=area.name,
                                                      indicator_name=indicator.name, republish=indicator.republish,
                                                      area_code=area.area, provider_name=indicator.provider_name,
                                                      provider_url=indicator.provider_url, short_name=area.short_name,
                                                      area_type=area.type)