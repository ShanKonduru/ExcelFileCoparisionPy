import pandas as pd
import numpy as np

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

        # Compare rows and columns
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

                if cell_value1 != cell_value2 and not (pd.isna(cell_value1) and pd.isna(cell_value2)):
                    col_name = df1.columns[col_index] if col_index < len(df1.columns) else df2.columns[col_index]
                    differences[(row_index, col_index)] = (col_name, cell_value1, cell_value2)

        # Check for missing columns
        missing_columns1 = set(df2.columns) - set(df1.columns)
        missing_columns2 = set(df1.columns) - set(df2.columns)
        for col_name in missing_columns1:
            differences[(None, df2.columns.get_loc(col_name))] = (col_name, None, "Missing Column")
        for col_name in missing_columns2:
            differences[(None, df1.columns.get_loc(col_name))] = (col_name, "Missing Column", None)

        return differences

    def compare_workbooks(self):
        workbook1_sheets = pd.ExcelFile(self.workbook1).sheet_names
        workbook2_sheets = pd.ExcelFile(self.workbook2).sheet_names

        all_differences = {}

        # Compare sheets present in workbook1 but not in workbook2
        for sheet in workbook1_sheets:
            if sheet not in workbook2_sheets:
                all_differences["Missing Sheets"] = all_differences.get("Missing Sheets", []) + [sheet]

        # Compare sheets present in workbook2 but not in workbook1
        for sheet in workbook2_sheets:
            if sheet not in workbook1_sheets:
                all_differences["Missing Sheets"] = all_differences.get("Missing Sheets", []) + [sheet]

        common_sheets = set(workbook1_sheets).intersection(workbook2_sheets)

        for sheet in common_sheets:
            differences = self.compare_sheets(sheet)
            if differences:
                all_differences[sheet] = differences

        # Categorize differences into buckets
        categorized_differences = {}
        for category, differences in all_differences.items():
            if category == "Missing Sheets":
                categorized_differences["Missing Sheets"] = differences
            else:
                for cell, values in differences.items():
                    col_name, value1, value2 = values
                    if pd.isna(value1) and pd.isna(value2):
                        continue
                    elif pd.isna(value1) or pd.isna(value2):
                        categorized_differences.setdefault("Missing Rows", []).append((category, cell, values))
                    elif isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
                        categorized_differences.setdefault("Numeric Edits", []).append((category, cell, values))
                    else:
                        categorized_differences.setdefault("Text Edits", []).append((category, cell, values))

        return categorized_differences

if __name__ == "__main__":
    workbook1_path = "workbook1.xlsx"
    workbook2_path = "workbook2.xlsx"

    comparator = ExcelComparator(workbook1_path, workbook2_path)
    result = comparator.compare_workbooks()

    if result:
        print("Differences found:")
        for category, differences in result.items():
            print(f"- {category}:")
            if category == "Missing Sheets":
                for sheet in differences:
                    print(f"  - Missing Sheet: {sheet}")
            else:
                for sheet, cell, values in differences:
                    print(f"  - Sheet '{sheet}': Cell {cell}: Column '{values[0]}', Values {values[1]} != {values[2]}")
    else:
        print("No differences found.")
