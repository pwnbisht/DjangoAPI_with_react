from pandas import DataFrame
from rest_framework.exceptions import ValidationError


def determine_csv_file_name(file_name):
    """
    Determine the CSV file name based on the provided file name.

    Args:
        file_name (str): Name of the CSV file.

    Returns:
        str: Determined CSV file name ('CSVFile1', 'CSVFile2'), or None if not recognized.
    """
    if 'csv1' in file_name.lower():
        return 'CSVFile1'
    elif 'csv2' in file_name.lower():
        return 'CSVFile2'
    else:
        return


def validate_columns_and_datatypes_csv(df, file_name: str):
    """
    Validate columns and datatypes for a CSV file.

    Args:
        df (DataFrame): Pandas DataFrame representing the CSV file.
        file_name (str): Name of the CSV file ('CSVFile1', 'CSVFile2').

    Raises:
        ValidationError: If validation fails.
    """
    expected_columns_and_datatypes = {
        'CSVFile1': {
            'Time': 'int64',
            'V1': 'float64',
            'V2': 'float64',
            'V3': 'float64',
            'V4': 'float64',
            'V5': 'float64',
            'V6': 'float64',
            'V7': 'float64',
            'V8': 'float64',
            'V9': 'float64',
            'V10': 'float64',
            'V11': 'float64',
            'V12': 'float64',
            'V13': 'float64',
            'V14': 'float64',
            'V15': 'float64',
            'V16': 'float64',
            'V17': 'float64',
            'V18': 'float64',
            'V19': 'float64',
            'V20': 'float64',
            'V21': 'float64',
            'V22': 'float64',
            'V23': 'float64',
            'V24': 'float64',
            'V25': 'float64',
            'V26': 'float64',
            'V27': 'float64',
            'V28': 'float64',
            'Amount': 'float64',
            'Class': 'int64',
        },
        'CSVFile2': {
            'Loan_ID': 'object',
            'loan_status': 'object',
            'Principal': 'int64',
            'terms': 'int64',
            'effective_date': 'object',
            'due_date': 'object',
            'paid_off_time': 'object',
            'past_due_days': 'float64',
            'age': 'int64',
            'education': 'object',
            'Gender': 'object',
        },
    }
    expected_columns = expected_columns_and_datatypes.get(file_name, expected_columns_and_datatypes[file_name])

    # Check if all expected columns are present
    if not set(expected_columns.keys()).issubset(df.columns):
        raise ValidationError(f"Missing one or more expected columns for {file_name}.")

    # Check datatypes for each column
    for column, expected_datatype in expected_columns.items():
        if str(df[column].dtype) != expected_datatype:
            raise ValidationError(f"Invalid datatype for {column}. Expected {expected_datatype}, found {df[column].dtype}.")


def validate_columns_and_datatypes_excel(df):
    """
    Validate columns and datatypes for an Excel file.

    Args:
        df (DataFrame): Pandas DataFrame representing the Excel file.

    Raises:
        ValidationError: If validation fails.
    """
    expected_columns_and_datatypes = {
        'ExcelFile': {
            'Loan_ID': 'object',
            'Gender': 'object',
            'Married': 'object',
            'Dependents': 'object',
            'Education': 'object',
            'Self_Employed': 'object',
            'ApplicantIncome': 'int64',
            'CoapplicantIncome': 'int64',
            'LoanAmount': 'int64',
            'Loan_Amount_Term': 'int64',
            'Credit_History': 'int64',
            'Property_Area': 'object',
        }
    }

    expected_columns = expected_columns_and_datatypes.get('ExcelFile')

    # Check if all expected columns are present
    if not set(expected_columns.keys()).issubset(df.columns):
        raise ValidationError("Missing one or more expected columns for Excel file.")

    # Check datatypes for each column
    for column, expected_datatype in expected_columns.items():
        if str(df[column].dtype) != expected_datatype:
            raise ValidationError(
                f"Invalid datatype for {column}. Expected {expected_datatype}, found {df[column].dtype}.")
