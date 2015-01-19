import xlrd

__author__ = 'Miguel'


class Parser(object):

    def __init__(self, log, config):
        self._log = log
        self._config = config

    def run(self):
        self._log.info("Running parser")
        sheet = self.get_data_sheet()
        self.retrieve_data(sheet)
        self._log.info("Parsing finished")

    def get_data_sheet(self):
        file_name = self._config.get("DATA_ACCESS", "FILE_NAME")
        book = xlrd.open_workbook(file_name)
        sheet_number = self._config.getint("DATA_ACCESS", "SHEET_NUMBER")
        sheet = book.sheet_by_index(sheet_number)
        return sheet

    def retrieve_data(self, sheet):
        countries_column = self._config.getint("DATA_ACCESS", "COUNTRIES_COLUMN")
        indicator_columns_range = self._config.get("DATA_ACCESS", "INDICATOR_COLUMNS_RANGE").split(", ")
        indicator_names_row = self._config.getint("DATA_ACCESS", "INDICATOR_NAMES_ROW")
        for row_number in range(1, sheet.nrows):
            country_name = sheet.cell(row_number, countries_column).value
            for column_number in range(int(indicator_columns_range[0]), int(indicator_columns_range[1]) + 1):
                indicator_name = sheet.cell(indicator_names_row, column_number).value
                observation_value = sheet.cell(row_number, column_number).value
                print country_name + " " + indicator_name + " " + str(observation_value)