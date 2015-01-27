from webindex.domain.model.indicator.indicator import *

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