import xlrd
from application.a4aiFetcher.parsing.excel_model.excel_indicator import ExcelIndicator
from infrastructure.mongo_repos.indicator_repository import IndicatorRepository
from application.a4aiFetcher.parsing.excel2dom import Excel2Dom

__author__ = 'Miguel'


class Parser(object):

    def __init__(self, log, config):
        self._log = log
        self._config = config
        self._excel_indicators = []

    def run(self):
        self._log.info("Running parser")
        indicator_sheet, data_sheet = self.initialize_sheets()
        indicator_repo = self.initialize_repositories()
        self.retrieve_indicators(indicator_sheet)
        self.store_indicators(indicator_repo)
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

    def initialize_repositories(self):
        indicator_repo = IndicatorRepository(self._config.get("CONNECTION", "MONGO_IP"))
        return indicator_repo

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
            retrieved_code = indicator_sheet.cell(row_number, code_column).value
            code = retrieved_code.upper().replace(" ", "_")
            name = indicator_sheet.cell(row_number, name_column).value
            _type = indicator_sheet.cell(row_number, type_column).value
            subindex_name = indicator_sheet.cell(row_number, subindex_column).value
            indicator = ExcelIndicator(code, name, _type, subindex_name)
            self._excel_indicators.append(indicator)
            print indicator.code

    def store_indicators(self, indicator_repo):
        for excel_indicator in self._excel_indicators:
            indicator = Excel2Dom.excel_indicator_to_dom(excel_indicator)
            indicator_uri = self._config.get("OTHERS", "HOST") + indicator.code
            indicator_repo.insert_indicator(indicator,
                                            indicator_uri=indicator_uri,
                                            index_name="INDEX",
                                            subindex_name=excel_indicator.subindex_name,
                                            provider_name=self._config.get("OTHERS", "WF_NAME"),
                                            provider_url=self._config.get("OTHERS", "WF_URL"))

    def retrieve_data(self, data_sheet):
        countries_column = self._config.getint("DATA_ACCESS", "COUNTRIES_COLUMN")
        indicator_columns_range = self._config.get("DATA_ACCESS", "INDICATOR_COLUMNS_RANGE").split(", ")
        indicator_names_row = self._config.getint("DATA_ACCESS", "INDICATOR_NAMES_ROW")

        for row_number in range(1, data_sheet.nrows):
            country_name = data_sheet.cell(row_number, countries_column).value
            for column_number in range(int(indicator_columns_range[0]), int(indicator_columns_range[1]) + 1):
                indicator_name = data_sheet.cell(indicator_names_row, column_number).value
                observation_value = data_sheet.cell(row_number, column_number).value