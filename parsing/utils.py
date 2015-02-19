from a4ai.domain.model.indicator.indicator import *
from a4ai.domain.model.observation.observation import *
from a4ai.domain.model.observation.year import Year

__author__ = 'Miguel'


def string_to_bool(string):
    return string in ["True", "true"]


def excel_indicator_to_dom(excel_indicator):
    indicator = create_indicator(type=excel_indicator.type,
                                 name=excel_indicator.name,
                                 indicator=excel_indicator.code,
                                 republish=excel_indicator.republishable,
                                 description=excel_indicator.name,
                                 provider_name=excel_indicator.provider_name,
                                 provider_url=excel_indicator.provider_url)
    return indicator


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
                                     year=Year(2014),
                                     continent=area.area)
    return observation