__author__ = 'Miguel'


class IndicatorData(object):

    def __init__(self, indicator_code, year, value, provider_name, provider_url):
        self._indicator_code = indicator_code
        self._year = year
        self._value = value
        self._provider_name = provider_name
        self._provider_url = provider_url

    @property
    def indicator_code(self):
        return self._indicator_code

    @property
    def year(self):
        return self._year

    @property
    def value(self):
        return self._value

    @property
    def provider_name(self):
        return self._provider_name

    @property
    def provider_url(self):
        return self._provider_url