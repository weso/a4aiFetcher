__author__ = 'Miguel'

class ExcelIndicator(object):

    def __init__(self, _code, _name, _type, _subindex_code):
        self._code = _code
        self._name = _name
        self._type = _type
        self._subindex_code = _subindex_code

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def subindex_code(self):
        return self._subindex_code