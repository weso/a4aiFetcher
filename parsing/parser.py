import xlrd

from application.a4aiFetcher.parsing.utils import *
from application.a4aiFetcher.parsing.excel_model.excel_indicator import ExcelIndicator

from infrastructure.mongo_repos.indicator_repository import IndicatorRepository
from infrastructure.mongo_repos.observation_repository import ObservationRepository
from infrastructure.mongo_repos.area_repository import AreaRepository


__author__ = 'Miguel'


class Parser(object):

    def __init__(self, log, config):
        self._log = log
        self._config = config
        self._indicator_repo, self._observation_repo, self._area_repo = self.initialize_repositories()

    def run(self):
        self._log.info("Running parser")
        indicator_sheet, index_subindex_sheet = self.initialize_sheets()
        indicator_repo, observation_repo, area_repo = self.initialize_repositories()
        self.retrieve_indicators(indicator_sheet)
        self.store_indicators(indicator_repo)

        self._log.info("Parsing finished")

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


