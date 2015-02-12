from infrastructure.mongo_repos.area_repository import AreaRepository
from rest_client import *

__author__ = 'Miguel'


class Enricher(object):

    def __init__(self, log, config):
        self._log = log
        self._config = config
        self._area_repo = AreaRepository(self._config.get("CONNECTION", "MONGO_IP"))

    def run(self):
        self._retrieve_indicator_values()
        self._enrich()

    def retrieve_indicator_values(self):
        pass

    def enrich(self):
        pass