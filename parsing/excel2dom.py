from webindex.domain.model.indicator.indicator import *
from webindex.domain.model.observation.observation import *
from utility.time import utc_now
from webindex.domain.model.observation.year import Year

__author__ = 'Miguel'


class Excel2Dom(object):

    @staticmethod
    def excel_indicator_to_dom(excel_indicator):
        indicator = create_indicator(type=excel_indicator.type,
                                     name=excel_indicator.name,
                                     indicator=excel_indicator.code,
                                     republish=excel_indicator.republishable,
                                     description=excel_indicator.name,
                                     provider_name=excel_indicator.provider_name,
                                     provider_url=excel_indicator.provider_url)
        return indicator

    @staticmethod
    def excel_observation_to_dom(excel_observation, area, indicator):
        observation = create_observation(value=excel_observation.value,
                                         republish=indicator.republish,
                                         area=area.iso3,
                                         area_name=area.name,
                                         indicator=indicator.indicator,
                                         indicator_name=indicator.name,
                                         provider_name=indicator.provider_name,
                                         provider_url=indicator.provider_url,
                                         short_name=area.short_name,
                                         year=Year(2013),
                                         continent=area.area)
        return observation