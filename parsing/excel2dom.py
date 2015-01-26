from webindex.domain.model.indicator.indicator import *

__author__ = 'Miguel'


class Excel2Dom(object):

    @staticmethod
    def excel_indicator_to_dom(excel_indicator):
        indicator = create_indicator(_type=excel_indicator.type,
                                     label=excel_indicator.name,
                                     code=excel_indicator.code,
                                     republish=True,
                                     comment=excel_indicator.name)
        return indicator