import xlrd
from application.a4aiFetcher.parsing.excel_model.excel_indicator import ExcelIndicator

__author__ = 'Miguel'


class Parser(object):

    def __init__(self, log, config):
        self._log = log
        self._config = config
        self._indicators = []

    def run(self):
        self._log.info("Running parser")
        indicator_sheet, data_sheet = self.initialize_sheets()
        self.retrieve_indicators(indicator_sheet)
        self.store_indicators()
        self.retrieve_data(data_sheet)
        self._log.info("Parsing finished")

    def initialize_sheets(self):
        structure_file_name = self._config.get("STRUCTURE_ACCESS", "FILE_NAME")
        data_file_name = self._config.get("DATA_ACCESS", "FILE_NAME")

        indicator_sheet_number = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_SHEET_NUMBER")
        data_sheet_number = self._config.getint("DATA_ACCESS", "SHEET_NUMBER")

        indicator_sheet = self.get_sheet(structure_file_name, indicator_sheet_number)
        data_sheet = self.get_sheet(data_file_name, data_sheet_number)
        return indicator_sheet, data_sheet

    @staticmethod
    def get_sheet(file_name, sheet_number):
        book = xlrd.open_workbook(file_name)
        sheet = book.sheet_by_index(sheet_number)
        return sheet

    def retrieve_indicators(self, indicator_sheet):
        code_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_CODE_COLUMN")
        name_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_NAME_COLUMN")
        type_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_TYPE_COLUMN")
        subindex_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_SUBINDEX_COLUMN")
        start_row = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_START_ROW")

        for row_number in range(start_row, indicator_sheet.nrows):
            code = indicator_sheet.cell(row_number, code_column).value
            name = indicator_sheet.cell(row_number, name_column).value
            _type = indicator_sheet.cell(row_number, type_column).value
            subindex_code = indicator_sheet.cell(row_number, subindex_column).value
            indicator = ExcelIndicator(code, name, _type, subindex_code)
            self._indicators.append(indicator)
            print indicator.code

    def store_indicators(self):
        pass

    def retrieve_data(self, data_sheet):
        countries_column = self._config.getint("DATA_ACCESS", "COUNTRIES_COLUMN")
        indicator_columns_range = self._config.get("DATA_ACCESS", "INDICATOR_COLUMNS_RANGE").split(", ")
        indicator_names_row = self._config.getint("DATA_ACCESS", "INDICATOR_NAMES_ROW")
        for row_number in range(1, data_sheet.nrows):
            country_name = data_sheet.cell(row_number, countries_column).value
            for column_number in range(int(indicator_columns_range[0]), int(indicator_columns_range[1]) + 1):
                indicator_name = data_sheet.cell(indicator_names_row, column_number).value
                observation_value = data_sheet.cell(row_number, column_number).value