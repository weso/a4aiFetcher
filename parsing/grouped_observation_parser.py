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
        self.store_grouped_observations(self._observation_repo, self._indicator_repo, self._area_repo)
        self._log.info("Finished parsing grouped observations")

    def initialize_grouped_obs_sheet(self):
        data_file_name = self._config.get("DATA_ACCESS", "FILE_NAME")
        index_subindex_sheet_number = self._config.getint("INDEX_SUBINDEX_OBSERVATIONS", "SHEET_NUMBER")
        index_subindex_sheet = self.get_sheet(data_file_name, index_subindex_sheet_number)
        return index_subindex_sheet

    def retrieve_grouped_observations(self, grouped_obs_sheet):
        countries_column = self._config.getint("INDEX_SUBINDEX_OBSERVATIONS", "COUNTRIES_COLUMN")
        indicator_columns_range = self._config.get("INDEX_SUBINDEX_OBSERVATIONS", "INDICATOR_COLUMNS_RANGE").split(", ")
        indicator_names_row = self._config.getint("INDEX_SUBINDEX_OBSERVATIONS", "INDICATOR_NAMES_ROW")
        ranking_column = self._config.getint("INDEX_SUBINDEX_OBSERVATIONS", "OVERALL_RANKING_COLUMN")

        for row_number in range(1, grouped_obs_sheet.nrows):
            country_name = grouped_obs_sheet.cell(row_number, countries_column).value
            for column_number in range(int(indicator_columns_range[0]), int(indicator_columns_range[1]) + 1):
                retrieved_indicator_code = grouped_obs_sheet.cell(indicator_names_row, column_number).value
                indicator_code = retrieved_indicator_code.upper()
                observation_value = grouped_obs_sheet.cell(row_number, column_number).value
                index_overall_ranking = None
                if indicator_code == "INDEX":
                    index_overall_ranking = int(grouped_obs_sheet.cell(row_number, ranking_column).value)
                observation = ExcelObservation(country_name, indicator_code, observation_value, index_overall_ranking)
                self._excel_grouped_observations.append(observation)

    def store_grouped_observations(self, observation_repo, indicator_repo, area_repo):
        for excel_observation in self._excel_grouped_observations:
            area = area_repo.find_by_name(excel_observation.country_name)
            indicator = indicator_repo.find_indicators_by_code(excel_observation.indicator_code)
            observation = excel_observation_to_dom(excel_observation, area, indicator)
            observation_uri = self._config.get("OTHERS", "HOST") + "observations/" + indicator.indicator + "/" \
                              + area.iso3 + "/" + str(observation.year.value)
            observation_repo.insert_observation(observation, observation_uri=observation_uri, area_iso3_code=area.iso3,
                                                indicator_code=indicator.indicator,
                                                year_literal=str(observation.year.value), area_name=area.name,
                                                indicator_name=indicator.name, republish=indicator.republish,
                                                area_code=area.area, provider_name=indicator.provider_name,
                                                provider_url=indicator.provider_url, short_name=area.short_name,
                                                area_type=area.type)