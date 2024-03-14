import pandas as pd

class ExcelComparator:
    def __init__(self, workbook1, workbook2):
        self.workbook1 = workbook1
        self.workbook2 = workbook2

    def compare_sheets(self, sheet_name):
        df1 = pd.read_excel(self.workbook1, sheet_name=sheet_name)
        df2 = pd.read_excel(self.workbook2, sheet_name=sheet_name)

        differences = {}
        for row_index in range(len(df1)):
            for col_index in range(len(df1.columns)):
                cell_value1 = df1.iloc[row_index, col_index]
                cell_value2 = df2.iloc[row_index, col_index]
                if cell_value1 != cell_value2:
                    col_name = df1.columns[col_index]
                    differences[(row_index, col_index)] = (col_name, cell_value1, cell_value2)

        return differences

    def compare_workbooks(self):
        workbook1_sheets = pd.ExcelFile(self.workbook1).sheet_names
        workbook2_sheets = pd.ExcelFile(self.workbook2).sheet_names
        common_sheets = set(workbook1_sheets).intersection(workbook2_sheets)

        all_differences = {}
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
            print(f"- Sheet '{sheet}':")
            for cell, values in differences.items():
                print(f"  - Cell {cell}: Column '{values[0]}', Values {values[1]} != {values[2]}")
    else:
        print("No differences found.")
