# relatorios/base/base_excel.py
import pandas as pd
from openpyxl.utils import get_column_letter

class BaseExcelReport:
    sheet_name = "Relatório"

    def __init__(self, queryset, fields):
        self.queryset = queryset
        self.fields = fields

    def get_dataframe(self):
        return pd.DataFrame(self.queryset.values(*self.fields))

    def autofit_columns(self, worksheet):
        for col in worksheet.columns:
            max_length = max(len(str(cell.value or "")) for cell in col)
            column_letter = get_column_letter(col[0].column)
            worksheet.column_dimensions[column_letter].width = max_length + 2

    def render(self, response):
        df = self.get_dataframe()

        with pd.ExcelWriter(response, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name=self.sheet_name)
            ws = writer.sheets[self.sheet_name]
            self.autofit_columns(ws)

        return response
