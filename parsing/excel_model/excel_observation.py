__author__ = 'Miguel'


class ExcelObservation(object):

    def __init__(self, country_name, indicator_code, _value, index_overall_ranking):
        self._country_name = country_name
        self._indicator_code = indicator_code
        self._value = _value
        self._index_overall_ranking = index_overall_ranking

    @property
    def country_name(self):
        return self._country_name

    @property
    def indicator_code(self):
        return self._indicator_code

    @property
    def value(self):
        return self._value

    @property
    def index_overall_ranking(self):
        return self._index_overall_ranking