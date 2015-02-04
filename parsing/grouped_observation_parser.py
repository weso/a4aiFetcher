from application.a4aiFetcher.parsing.parser import Parser
from application.a4aiFetcher.parsing.utils import *
from application.a4aiFetcher.parsing.excel_model.excel_observation import ExcelObservation

__author__ = 'Miguel'


class GroupedObservationParser(Parser):

    def __init__(self, log, config):
        super(GroupedObservationParser, self).__init__(log, config)
        self._excel_grouped_observations = []

    def run(self):
        self._log.info("Running grouped observation parser")
        grouped_obs_sheet = self.initialize_grouped_obs_sheet()
        self.retrieve_grouped_observations(grouped_obs_sheet)
        self.store_grouped_observations()
        self.rank_observations_by_type()
        self._log.info("Finished parsing grouped observations")

    def initialize_grouped_obs_sheet(self):
        data_file_name = self._config.get("DATA_ACCESS", "FILE_NAME")
        grouped_sheet_number = self._config.getint("GROUPED_OBSERVATIONS", "SHEET_NUMBER")
        grouped_obs_sheet = self.get_sheet(data_file_name, grouped_sheet_number)
        return grouped_obs_sheet

    def retrieve_grouped_observations(self, grouped_obs_sheet):
        country_column = self._config.getint("GROUPED_OBSERVATIONS", "COUNTRY_COLUMN")
        indicator_column = self._config.getint("GROUPED_OBSERVATIONS", "INDICATOR_COLUMN")
        ranking_column = self._config.getint("GROUPED_OBSERVATIONS", "RANKING_COLUMN")
        indicator_names_row = self._config.getint("GROUPED_OBSERVATIONS", "INDICATOR_NAMES_ROW")
        indicator_quantity = self._config.getint("GROUPED_OBSERVATIONS", "INDICATOR_QUANTITY")

        for row_number in range(1, grouped_obs_sheet.nrows):
            column_offset = 0
            for indicator_num in range(0, indicator_quantity):
                country_name = grouped_obs_sheet.cell(row_number, country_column + column_offset).value
                retrieved_indicator_code = grouped_obs_sheet.cell(indicator_names_row,
                                                                  indicator_column + column_offset).value
                indicator_code = retrieved_indicator_code.upper()
                ranking = grouped_obs_sheet.cell(row_number, ranking_column + column_offset).value
                observation_value = grouped_obs_sheet.cell(row_number, indicator_column + column_offset).value

                observation = ExcelObservation(country_name, indicator_code, observation_value, ranking=ranking)
                self._excel_grouped_observations.append(observation)
                column_offset += 4

    def store_grouped_observations(self):
        for excel_observation in self._excel_grouped_observations:
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
                                                      area_type=area.type, ranking=excel_observation.ranking)

    def rank_observations_by_type(self):
        indicators = self._indicator_repo.find_indicators()
        for indicator in indicators:
            emerging_observations = self._observation_repo.find_observations(indicator_code=indicator.indicator,
                                                                             area_type="Emerging")
            developing_observations = self._observation_repo.find_observations(indicator_code=indicator.indicator,
                                                                               area_type="Developing")
            emerging_ordered = sorted(emerging_observations, key=lambda observation: observation.value)
            developing_ordered = sorted(developing_observations, key=lambda observation: observation.value)
            rank_emerging = len(emerging_ordered)
            rank_developing = len(developing_ordered)
            for emerging_obs in emerging_ordered:
                self._observation_repo.update_observation_ranking_type(emerging_obs, rank_emerging)
                rank_emerging -= 1
            for developing_obs in developing_ordered:
                self._observation_repo.update_observation_ranking_type(developing_obs, rank_developing)
                rank_developing -= 1
