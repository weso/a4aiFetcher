from application.a4aiFetcher.enrichment.indicator_data import IndicatorData
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
                    print "\t\t" + dict_key + " " + last_year_data['date'] + "-->" + str(last_year_data['value'])
                else:
                    print "\t\t" + area.iso3 + " has no values"
        self._log.info("\tFinished data from datasource")
        print "\tFinished data from datasource"

    def enrich(self):
        self._log.info("\tUpdating areas")
        print "\tUpdating areas"

        indicator_codes = self._config.get("ENRICHMENT", "WB_INDICATOR_CODES").split(", ")
        areas = self._area_repo.find_countries("iso3")
        provider_name = self._config.get("ENRICHMENT", "WB_PROVIDER_NAME")

        for area in areas:
            indicators = []
            print "\t\t" + area.iso3
            for indicator_code in indicator_codes:
                try:
                    data = self._retrieved_data[area.iso3 + "-" + indicator_code]
                    year = data['date']
                    value = data['value']
                    provider_url = self._config.get("ENRICHMENT", "WB_PROVIDER_URL_PATTERN").replace("{INDICATOR_CODE}",
                                                                                                     indicator_code)
                    indicator_data = IndicatorData(indicator_code.replace(".", "_"), year, value, provider_name, provider_url)
                    indicators.append(indicator_data)
                    print "\t\t\t" + indicator_data.indicator_code.replace(".", "_") + " " + indicator_data.year + " " + indicator_data.value + " " + indicator_data.provider_url
                except KeyError:
                    print "\t\t\tNo data for " + indicator_code
            self._area_repo.enrich_country(area.iso3, indicators)
        self._log.info("\tFinished updating areas")
        print "\tFinished updating areas"