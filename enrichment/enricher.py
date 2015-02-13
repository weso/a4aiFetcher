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
        self._log.info("Enriching areas")
        print "Enriching areas"

        self.retrieve_indicator_values()
        self.enrich()

        self._log.info("Finished enriching areas")
        print "Finished enriching areas"

    def retrieve_indicator_values(self):
        self._log.info("\tRetrieving data from datasource")
        print "\tRetrieving data from datasource"
        uri_pattern = self._config.get("ENRICHMENT", "WB_INDICATOR_URL_QUERY_PATTERN")
        indicator_codes = self._config.get("ENRICHMENT", "WB_INDICATOR_CODES").split(", ")
        areas = self._area_repo.find_countries("iso3")

        for indicator_code in indicator_codes:
            for area in areas:
                uri = uri_pattern.replace("{ISO3}", area.iso3).replace("{INDICATOR_CODE}", indicator_code)
                response = get_json(uri, {"format": "json"})
                value = None
                year_index = 0
                while value is None and year_index < len(response[1]):
                    last_year_data = response[1][year_index]
                    value = last_year_data['value']
                    year_index += 1
                if value is not None:
                    dict_key = area.iso3 + "-" + indicator_code
                    self._retrieved_data[dict_key] = last_year_data
                    print dict_key + " " + last_year_data['date'] + "-->" + str(last_year_data['value'])
        self._log.info("\tFinished data from datasource")
        print "\tFinished data from datasource"

    def enrich(self):
        indicator_codes = self._config.get("ENRICHMENT", "WB_INDICATOR_CODES").split(", ")
        areas = self._area_repo.find_countries("iso3")

        for area in areas:
            indicators = []
            for indicator_code in indicator_codes:
                data = self._retrieved_data[area.iso3 + "-" + indicator_code]
