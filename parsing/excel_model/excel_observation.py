__author__ = 'Miguel'


class ExcelObservation(object):

    def __init__(self, country_name, indicator_code, _value, ranking=None, ranking_type=None):
        self._country_name = country_name
        self._indicator_code = indicator_code
        self._value = _value
        self._ranking = ranking
        self._ranking_type = ranking_type

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
    def ranking(self):
        return self._ranking

    @ranking.setter
    def ranking(self, ranking):
        self._ranking = ranking

    @property
    def ranking_type(self):
        return self._ranking_type

    @ranking_type.setter
    def ranking_type(self, ranking_type):
        self._ranking_type = ranking_type