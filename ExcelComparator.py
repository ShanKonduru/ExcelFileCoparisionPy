import pandas as pd

class ExcelComparator:
    def __init__(self, workbook1, workbook2):
        self.workbook1 = workbook1
        self.workbook2 = workbook2

    def compare_sheets(self, sheet_name):
        df1 = pd.read_excel(self.workbook1, sheet_name=sheet_name)
        df2 = pd.read_excel(self.workbook2, sheet_name=sheet_name)

        differences = {}
        max_rows = max(len(df1), len(df2))
        max_cols = max(len(df1.columns), len(df2.columns))

        for row_index in range(max_rows):
            for col_index in range(max_cols):
                if row_index < len(df1) and col_index < len(df1.columns):
                    cell_value1 = df1.iloc[row_index, col_index]
                else:
                    cell_value1 = None
                if row_index < len(df2) and col_index < len(df2.columns):
                    cell_value2 = df2.iloc[row_index, col_index]
                else:
                    cell_value2 = None

                if cell_value1 != cell_value2:
                    col_name = df1.columns[col_index] if col_index < len(df1.columns) else df2.columns[col_index]
                    differences[(row_index, col_index)] = (col_name, cell_value1, cell_value2)

        return differences

    def compare_workbooks(self):
        workbook1_sheets = pd.ExcelFile(self.workbook1).sheet_names
        workbook2_sheets = pd.ExcelFile(self.workbook2).sheet_names

        all_differences = {}

        # Compare sheets present in workbook1 but not in workbook2
        for sheet in workbook1_sheets:
            if sheet not in workbook2_sheets:
                all_differences[sheet] = "Sheet is present in workbook1 but not in workbook2"

        # Compare sheets present in workbook2 but not in workbook1
        for sheet in workbook2_sheets:
            if sheet not in workbook1_sheets:
                all_differences[sheet] = "Sheet is present in workbook2 but not in workbook1"

        common_sheets = set(workbook1_sheets).intersection(workbook2_sheets)

        for sheet in common_sheets:
            differences = self.compare_sheets(sheet)
            if differences:
                all_differences[sheet] = differences

        return all_differences

if __name__ == "__main__":
    workbook1_path = "workbook1.xlsx"
    workbook2_path = "workbook2.xlsx"

    comparator = ExcelComparator(workbook1_path, workbook2_path)
    result = comparator.compare_workbooks()

    if result:
        print("Differences found:")
        for sheet, differences in result.items():
            if isinstance(differences, str):
                print(f"- Sheet '{sheet}': {differences}")
            else:
                print(f"- Sheet '{sheet}':")
                for cell, values in differences.items():
                    print(f"  - Cell {cell}: Column '{values[0]}', Values {values[1]} != {values[2]}")
    else:
        print("No differences found.")
