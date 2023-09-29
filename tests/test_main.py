import pandas as pd
from main import DataGenerator
import datetime
import pytest


class TestDataGenerator:
    # Tests that checkDate method successfully converts a valid date string into a pandas datetime object
    def test_checkDate_valid_date(self, mocker):
        # Mock the pd.to_datetime function to return a known datetime object
        mocker.patch('pandas.to_datetime',
                     return_value=pd.Timestamp('2022-01-01'))
        # Create an instance of DataGenerator
        data_generator = DataGenerator(
            100, 'data', 'test_conf.csv', 'csv', 'm')
        # Call the checkDate method with a valid date string
        result = data_generator.checkDate('2022-01-01')
        # Assert that the result is the expected datetime object
        assert result == pd.Timestamp('2022-01-01')
    # Tests that checkDate method returns None when an invalid date string is passed as input

    def test_checkDate_invalid_date(self, mocker):
        # Mock the pd.to_datetime function to raise an exception
        mocker.patch('pandas.to_datetime', side_effect=Exception)
        # Create an instance of DataGenerator
        data_generator = DataGenerator(
            100, 'data', 'test_conf.csv', 'csv', 'm')
        # Call the checkDate method with an invalid date string
        result = data_generator.checkDate('2022-13-01')
        # Assert that the result is None
        assert result is None
