import xlrd
from infrastructure.mongo_repos.indicator_repository import IndicatorRepository
from infrastructure.mongo_repos.observation_repository import ObservationRepository
from infrastructure.mongo_repos.area_repository import AreaRepository

__author__ = 'Miguel'

"""
This superclass models the various parsers that will retrieve and store the data
and implements their common functions
"""


class Parser(object):

    def __init__(self, log, config):
        self._log = log
        self._config = config
        self._indicator_repo, self._observation_repo, self._area_repo = self._initialize_repositories()

    def _initialize_repositories(self):
        indicator_repo = IndicatorRepository(self._config.get("CONNECTION", "MONGO_IP"))
        observation_repo = ObservationRepository(self._config.get("CONNECTION", "MONGO_IP"))
        area_repo = AreaRepository(self._config.get("CONNECTION", "MONGO_IP"))
        return indicator_repo, observation_repo, area_repo

    """

    """
    @staticmethod
    def _get_sheet(file_name, sheet_number):
        book = xlrd.open_workbook(file_name)
        sheet = book.sheet_by_index(sheet_number)
        return sheet


