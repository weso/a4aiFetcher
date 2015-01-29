import xlrd
from application.a4aiFetcher.parsing.excel2dom import Excel2Dom
from application.a4aiFetcher.parsing.utils import *
from application.a4aiFetcher.parsing.excel_model.excel_indicator import ExcelIndicator
from application.a4aiFetcher.parsing.excel_model.excel_observation import ExcelObservation
from infrastructure.mongo_repos.indicator_repository import IndicatorRepository
from infrastructure.mongo_repos.observation_repository import ObservationRepository
from infrastructure.mongo_repos.area_repository import AreaRepository


__author__ = 'Miguel'


class Parser(object):

    def __init__(self, log, config):
        self._log = log
        self._config = config
        self._excel_indicators = []
        self._excel_observations = []

    def run(self):
        self._log.info("Running parser")
        indicator_sheet, index_subindex_sheet = self.initialize_sheets()
        indicator_repo, observation_repo, area_repo = self.initialize_repositories()
        # self.retrieve_indicators(indicator_sheet)
        # self.store_indicators(indicator_repo)
        self.retrieve_grouped_observations(index_subindex_sheet)
        self.store_grouped_observations(observation_repo, indicator_repo, area_repo)
        self._log.info("Parsing finished")

    def initialize_sheets(self):
        structure_file_name = self._config.get("STRUCTURE_ACCESS", "FILE_NAME")
        data_file_name = self._config.get("DATA_ACCESS", "FILE_NAME")

        indicator_sheet_number = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_SHEET_NUMBER")
        index_subindex_sheet_number = self._config.getint("INDEX_SUBINDEX_OBSERVATIONS", "SHEET_NUMBER")

        indicator_sheet = self.get_sheet(structure_file_name, indicator_sheet_number)
        index_subindex_sheet = self.get_sheet(data_file_name, index_subindex_sheet_number)
        return indicator_sheet, index_subindex_sheet

    def initialize_repositories(self):
        indicator_repo = IndicatorRepository(self._config.get("CONNECTION", "MONGO_IP"))
        observation_repo = ObservationRepository(self._config.get("CONNECTION", "MONGO_IP"))
        area_repo = AreaRepository(self._config.get("CONNECTION", "MONGO_IP"))
        return indicator_repo, observation_repo, area_repo

    @staticmethod
    def get_sheet(file_name, sheet_number):
        book = xlrd.open_workbook(file_name)
        sheet = book.sheet_by_index(sheet_number)
        return sheet

    def retrieve_indicators(self, indicator_sheet):
        code_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_CODE_COLUMN")
        name_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_NAME_COLUMN")
        type_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_TYPE_COLUMN")
        subindex_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_SUBINDEX_COLUMN")
        start_row = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_START_ROW")
        provider_name_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_PROVIDER_NAME_COLUMN")
        provider_url_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_PROVIDER_URL_COLUMN")
        republishable_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_REPUBLISHABLE_COLUMN")

        for row_number in range(start_row, indicator_sheet.nrows):
            retrieved_code = indicator_sheet.cell(row_number, code_column).value
            code = retrieved_code.upper().replace(" ", "_")
            name = indicator_sheet.cell(row_number, name_column).value
            _type = indicator_sheet.cell(row_number, type_column).value
            subindex_code = indicator_sheet.cell(row_number, subindex_column).value
            provider_name = indicator_sheet.cell(row_number, provider_name_column).value
            provider_url = indicator_sheet.cell(row_number, provider_url_column).value
            retrieved_republishable = indicator_sheet.cell(row_number, republishable_column).value
            republishable = string_to_bool(retrieved_republishable)
            indicator = ExcelIndicator(code, name, _type, subindex_code, provider_name, provider_url, republishable)
            self._excel_indicators.append(indicator)

    def store_indicators(self, indicator_repo):
        for excel_indicator in self._excel_indicators:
            indicator = Excel2Dom.excel_indicator_to_dom(excel_indicator)
            indicator_uri = self._config.get("OTHERS", "HOST") + indicator.indicator
            indicator_repo.insert_indicator(indicator,
                                            indicator_uri=indicator_uri,
                                            index_name="INDEX",
                                            subindex_name=excel_indicator.subindex_code,
                                            provider_name=indicator.provider_name,
                                            provider_url=indicator.provider_url)

    def retrieve_grouped_observations(self, index_subindex_sheet):
        countries_column = self._config.getint("INDEX_SUBINDEX_OBSERVATIONS", "COUNTRIES_COLUMN")
        indicator_columns_range = self._config.get("INDEX_SUBINDEX_OBSERVATIONS", "INDICATOR_COLUMNS_RANGE").split(", ")
        indicator_names_row = self._config.getint("INDEX_SUBINDEX_OBSERVATIONS", "INDICATOR_NAMES_ROW")
        ranking_column = self._config.getint("INDEX_SUBINDEX_OBSERVATIONS", "OVERALL_RANKING_COLUMN")

        for row_number in range(1, index_subindex_sheet.nrows):
            country_name = index_subindex_sheet.cell(row_number, countries_column).value
            for column_number in range(int(indicator_columns_range[0]), int(indicator_columns_range[1]) + 1):
                retrieved_indicator_code = index_subindex_sheet.cell(indicator_names_row, column_number).value
                indicator_code = retrieved_indicator_code.upper()
                observation_value = index_subindex_sheet.cell(row_number, column_number).value
                index_overall_ranking = None
                if indicator_code == "INDEX":
                    index_overall_ranking = int(index_subindex_sheet.cell(row_number, ranking_column).value)
                observation = ExcelObservation(country_name, indicator_code, observation_value, index_overall_ranking)
                self._excel_observations.append(observation)

    def store_grouped_observations(self, observation_repo, indicator_repo, area_repo):
        indicators = indicator_repo.find_indicators_index() + indicator_repo.find_indicators_sub_indexes()
        areas = area_repo.find_countries("name")
        for excel_observation in self._excel_observations:
            area = area_repo.find_by_name(excel_observation.country_name)
            observation = Excel2Dom.excel_observation_to_dom()
