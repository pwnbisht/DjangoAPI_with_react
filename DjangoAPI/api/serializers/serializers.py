import mimetypes
from django.core.exceptions import ValidationError
from rest_framework import serializers
import pandas as pd
from api.models import User, UserFiles
from api.utils.filevalidations import determine_csv_file_name, validate_columns_and_datatypes_csv, \
    validate_columns_and_datatypes_excel


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create a new user with the provided data.

        Args:
            validated_data: Validated data for user creation.

        Returns:
            User: Newly created user instance.
        """
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserFilesSerializer(serializers.ModelSerializer):
    """
    Serializer for handling user files.
    """
    class Meta:
        model = UserFiles
        fields = ['user', 'file1', 'file2', 'file3']

    def validate(self, data):
        """
        Validate the uploaded files.

        Args:
            data: Dictionary containing file data.

        Raises:
            ValidationError: If validation fails.

        Returns:
            dict: Validated data.
        """

        # Check if at least one file is uploaded
        if not any(data.get(f) for f in ['file1', 'file2', 'file3']):
            raise ValidationError("At least one file must be uploaded.")

        # Validate each file individually
        for field_name in ['file1', 'file2', 'file3']:
            file_value = data.get(field_name)
            if file_value:
                self.validate_file(file_value)

        return data

    def validate_file(self, value):
        """
        Validate an individual file. and only accept .csv or excel(.xls,.xlsx) file.
        """
        allowed_formats = ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml'
                                                       '.sheet', 'text/csv']
        # Determine MIME type and encoding of the file
        file_mime_type, encoding = mimetypes.guess_type(value.name)
        if not file_mime_type or file_mime_type not in allowed_formats:
            raise ValidationError("Only Excel (xls, xlsx) or CSV files are allowed.")

        file_extension = value.name.split('.')[-1].lower()
        if file_extension == 'csv':
            file_name = determine_csv_file_name(value.name)
            self.validate_csv(value, file_name)
        elif file_extension in ['xls', 'xlsx']:
            self.validate_excel(value)

    @staticmethod
    def validate_csv(value, filename):
        """
        Validate a CSV file.

        Args:
            value: CSV file data.
            filename: Name of the file.

        Raises:
            ValidationError: If validation fails.
        """
        try:
            # Read the CSV file
            df_chunks = pd.read_csv(value)
            # df_chunks = pd.read_csv(value, chunksize=1000)

            # Check if the CSV file is empty
            if df_chunks.empty:
                raise ValidationError(f"{filename} is empty.")

            # Check for missing values in columns
            if df_chunks.isnull().any().any():
                raise ValidationError(f"CSV file contains missing values in one or more columns in file {filename}")

            # Validate columns and datatypes
            validate_columns_and_datatypes_csv(df_chunks, filename)
        except pd.errors.EmptyDataError as e:
            pass
        except pd.errors.ParserError:
            raise ValidationError("Invalid CSV format.")

    @staticmethod
    def validate_excel(value):
        """
        Validate an Excel file.

        Args:
            value: Excel file data.

        Raises:
            ValidationError: If validation fails.
        """
        try:
            # Read the Excel file
            df = pd.read_excel(value, engine='openpyxl')
            # Check for missing values in columns
            if df.isnull().any().any():
                raise ValidationError("Excel file contains missing values in one or more columns.")

            # Validate columns and datatypes
            validate_columns_and_datatypes_excel(df)

        except Exception as e:
            raise ValidationError(f"Error loading or processing Excel file: {str(e)}")
