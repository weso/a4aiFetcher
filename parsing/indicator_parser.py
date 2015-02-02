from application.a4aiFetcher.parsing.parser import Parser
from application.a4aiFetcher.parsing.utils import *
from application.a4aiFetcher.parsing.excel_model.excel_indicator import ExcelIndicator

__author__ = 'Miguel'


class IndicatorParser(Parser):

    def __init__(self, log, config):
        super(IndicatorParser, self).__init__(log, config)
        self._excel_indicators = []

    def run(self):
        self._log.info("Running indicator parser")
        indicator_sheet = self.initialize_indicator_sheet()
        self.retrieve_indicators(indicator_sheet)
        self.store_indicators(self._indicator_repo)
        self._log.info("Finished parsing indicators")

    def initialize_indicator_sheet(self):
        structure_file_name = self._config.get("STRUCTURE_ACCESS", "FILE_NAME")
        indicator_sheet_number = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_SHEET_NUMBER")
        indicator_sheet = self.get_sheet(structure_file_name, indicator_sheet_number)
        return indicator_sheet

    def retrieve_indicators(self, indicator_sheet):
        code_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_CODE_COLUMN")
        name_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_NAME_COLUMN")
        type_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_TYPE_COLUMN")
        subindex_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_SUBINDEX_COLUMN")
        start_row = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_START_ROW")
        provider_name_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_PROVIDER_NAME_COLUMN")
        provider_url_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_PROVIDER_URL_COLUMN")
        republishable_column = self._config.getint("STRUCTURE_ACCESS", "INDICATOR_REPUBLISHABLE_COLUMN")

        for row_number in range(start_row, indicator_sheet.nrows):
            retrieved_code = indicator_sheet.cell(row_number, code_column).value
            code = retrieved_code.upper().replace(" ", "_")
            name = indicator_sheet.cell(row_number, name_column).value
            _type = indicator_sheet.cell(row_number, type_column).value
            subindex_code = indicator_sheet.cell(row_number, subindex_column).value
            provider_name = indicator_sheet.cell(row_number, provider_name_column).value
            provider_url = indicator_sheet.cell(row_number, provider_url_column).value
            retrieved_republishable = indicator_sheet.cell(row_number, republishable_column).value
            republishable = string_to_bool(retrieved_republishable)
            indicator = ExcelIndicator(code, name, _type, subindex_code, provider_name, provider_url, republishable)
            self._excel_indicators.append(indicator)

    def store_indicators(self, indicator_repo):
        for excel_indicator in self._excel_indicators:
            indicator = excel_indicator_to_dom(excel_indicator)
            indicator_uri = self._config.get("OTHERS", "HOST") + indicator.indicator
            indicator_repo.insert_indicator(indicator,
                                            indicator_uri=indicator_uri,
                                            index_name="INDEX",
                                            subindex_name=excel_indicator.subindex_code,
                                            provider_name=indicator.provider_name,
                                            provider_url=indicator.provider_url)