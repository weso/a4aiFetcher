from infrastructure.mongo_repos.area_repository import AreaRepository
from rest_client import *

__author__ = 'Miguel'


class Enricher(object):

    def __init__(self, log, config):
        self._log = log
        self._config = config
        self._area_repo = AreaRepository(self._config.get("CONNECTION", "MONGO_IP"))
        self._retrieved_data = dict()

    def run(self):
        self.retrieve_indicator_values()
        self.enrich()

    def retrieve_indicator_values(self):
        uri_pattern = self._config.get("ENRICHMENT", "WB_INDICATOR_URL_QUERY_PATTERN")
        indicator_codes = self._config.get("ENRICHMENT", "WB_INDICATOR_CODES").split(", ")
        areas = self._area_repo.find_countries("iso3")

        for indicator_code in indicator_codes:
            for area in areas:
                uri = uri_pattern.replace("{ISO3}", area.iso3).replace("{INDICATOR_CODE}", indicator_code)
                response = get_json(uri, {"format": "json"})
                last_year_data = response[1][0]
                dict_key = area.iso3 + "-" + indicator_code
                self._retrieved_data[dict_key] = last_year_data

    def enrich(self):
        pass