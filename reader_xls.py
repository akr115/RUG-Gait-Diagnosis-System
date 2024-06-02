import pandas as pd

# Load the Excel file
file_path = '/Users/emmanouilKalostypis/Downloads/LO.xlsx'
xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls, sheet_name='Blad1', header=None)

# Initialize lists for variable names and values
variable_names = []
variable_values = []

# Iterate through the entire column in steps of 3
for i in range(0, len(df) - 2, 3):
    if pd.notna(df.iloc[i + 1, 0]):  # Check if the name cell is not empty
        name = df.iloc[i + 1, 0]
        value = df.iloc[i + 2, 0]
        variable_names.append(name)
        variable_values.append(value)

# Example to print the lists
print("Variable names:", variable_names)
print("Variable values:", variable_values)
