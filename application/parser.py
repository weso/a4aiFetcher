import xlrd

__author__ = 'Miguel'


class Parser(object):

    def __init__(self, log, config):
        self._log = log
        self._config = config

    def run(self):
        self._log.info("Running parser")
        xlrd.open_workbook("data_file.xlsx")
        self._log.info("Parsing finished")