from webindex.domain.model.indicator.indicator import *

__author__ = 'Miguel'


class Excel2Dom(object):

    @staticmethod
    def excel_indicator_to_dom(excel_indicator):
        indicator = create_indicator(type=excel_indicator.type,
                                     name=excel_indicator.name,
                                     indicator=excel_indicator.code,
                                     republish=True,
                                     description=excel_indicator.name)
        return indicator