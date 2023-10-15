#!/usr/bin/env python

"""Tests for `sdgp` package."""
# import datetime
# import pytest
import unittest
from sdgp.sdgp import DataGenerator
import pandas as pd
# import numpy as np
import os
import time
from unittest.mock import patch


class TestSdgp(unittest.TestCase):
    """Tests for `sdgp` package."""

    def setUp(self):
        self.volume = 12000
        self.file = "tests/mock_table"
        self.conf_file = r'tests/test_assect/test_conf.csv'
        self.format = "csv"
        self.choice = "m"
        self.data_gen = DataGenerator(self.volume, self.file,
                                      self.conf_file, self.format, self.choice)

    def tearDown(self):
        pass

    def test_check_date(self):
        # Test checkDate method with a valid date
        date = "2022-01-01"
        result = self.data_gen.checkDate(date)
        self.assertIsInstance(result, pd.Timestamp)

        # Test checkDate method with an invalid date
        date = "2022-01-32"
        result = self.data_gen.checkDate(date)
        self.assertIsNone(result)

    def test_check_file(self):
        # Test checkFile method with a valid file
        path = r'tests/test_assect/test_conf.csv'
        result = self.data_gen.checkFile(path)
        self.assertIsInstance(result, pd.DataFrame)

        # Test checkFile method with an invalid file
        path = "tests/test_data/invalid.csv"
        with self.assertRaises(SystemExit):
            self.data_gen.checkFile(path)

    def test_generate_dates(self):
        # Test generateDates method with a valid date range
        s = "2022-01-01"
        e = "2022-12-31"
        format = "%Y-%m-%d"
        result = self.data_gen.generateDates(s, e, format)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), self.volume)

        # Test generateDates method with an invalid date range
        s = "2022-12-31"
        e = "2022-01-01"
        format = "%Y-%m-%d"
        with self.assertRaises(ValueError):
            self.data_gen.generateDates(s, e, format)

        # Test generateDates method with an invalid date range
        s = "2022-12-01"
        e = "2022-12-21"
        format = "%Y-%m-%hhdhh"
        with self.assertRaises(ValueError):
            self.data_gen.generateDates(s, e, format)

    def test_split_by_pipe(self):
        # Test splitByPipe method with a valid data string
        data = "preDate | 1 | 2 "
        result = self.data_gen.splitByPipe(data)
        self.assertIsInstance(result, list)
        self.assertEqual(result, ["preDate", "1", "2"])

    def test_save_in_csv(self):
        # Test saveInCSV method with a valid DataFrame
        self.data_gen.df_mock = pd.DataFrame({
            'a': [1, 2, 3]*self.volume,
            'b': [4, 5, 6]*self.volume,
            'c': [7, 8, 9]*self.volume
        })
        self.data_gen.saveInCSV()
        if os.path.exists(f'{self.file}\
_{self.choice}_{self.volume}.{self.format}'):
            os.remove(f'{self.file}\
_{self.choice}_{self.volume}.{self.format}')
            assert True
        else:
            assert False

        # Test saveInCSV method with an invalid DataFrame
        self.data_gen.df_mock = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.data_gen.saveInCSV()
        if os.path.exists(f'{self.file}\
_{self.choice}_{self.volume}.{self.format}'):
            os.remove(f'{self.file}\
_{self.choice}_{self.volume}.{self.format}')
            assert False
        else:
            assert True

    def test_save_in_parquet(self):
        # Test saveInParquet method with a valid DataFrame and file name
        self.data_gen.df_mock = pd.DataFrame({
            'a': [1, 2, 3]*self.volume,
            'b': [4, 5, 6]*self.volume,
            'c': [7, 8, 9]*self.volume
        })
        self.format = "parquet"
        self.data_gen.saveInParquet()
        if os.path.exists(f'{self.file}\
_{self.choice}_{self.volume}.{self.format}'):
            os.remove(f'{self.file}\
_{self.choice}_{self.volume}.{self.format}')
            assert True
        else:
            assert False
        # Test saveInParquet method with an invalid DataFrame and file name
        self.data_gen.df_mock = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.data_gen.saveInParquet()
        if os.path.exists(f'{self.file}\
_{self.choice}_{self.volume}.{self.format}'):
            os.remove(f'{self.file}\
_{self.choice}_{self.volume}.{self.format}')
            assert False
        else:
            assert True

    def test_add_random_duration(self):
        # Test addRandomDuration method with a valid start date
        start_date = self.data_gen.checkDate("2022-01-01")
        so = "1D"
        eo = "1W"
        format = "%Y-%m-%d %H:%M:%S"
        result = self.data_gen.addRandomDuration(start_date, so, eo, format)
        self.assertIsInstance(self.data_gen.checkDate(result), pd.Timestamp)

        # Test addRandomDuration method with an invalid start date
        start_date = self.data_gen.checkDate("2022-01-32")
        so = "1D"
        eo = "1W"
        format = "%Y-%m-%d %H:%M:%S"
        with self.assertRaises(ValueError):
            self.data_gen.addRandomDuration(start_date, so, eo, format)

    def test_check_duration(self):
        # Test check_date_duration with valid input
        start_duration = "1D"
        end_duration = "1W"
        result = self.data_gen.checkDuration(start_duration, end_duration)
        self.assertTrue(result)

        # Test check_date_duration with invalid input
        start_duration = "1W"
        end_duration = "1D"
        with self.assertRaises(ValueError):
            self.data_gen.checkDuration(start_duration, end_duration)

    def test_check_format(self):
        # Test check_date_format with valid input
        date_format = "%Y-%m-%d %H:%M:%S"
        result = self.data_gen.checkFormat(date_format)
        self.assertTrue(result)

        # Test check_date_format with invalid input
        date_format = "%Y-%m-%d %H:%M:%Sgdf%Z"
        with self.assertRaises(ValueError):
            self.data_gen.checkFormat(date_format)

    def test_conf_file(self):
        with self.assertRaises(ValueError):
            self.data_gen.checkFormat(DataGenerator(
                volume=1000, file="test_data",
                conf_file=r'tests/test_assect/test_conf_ng.csv',
                format="csv", choice="m"))

    def test_clock(self):
        # Create a DataGenerator instance
        data_gen = DataGenerator(volume=1000, file="test_data",
                                 conf_file=r'tests/test_assect/test_conf.csv',
                                 format="csv", choice="m")

        # Call a method that takes some time to execute
        start_time = time.time()
        data_gen.generateMockData()
        if os.path.exists(f'{data_gen.file}\
_{data_gen.choice}_{data_gen.volume}.{data_gen.outputFormat}'):

            os.remove(f'{data_gen.file}\
_{data_gen.choice}_{data_gen.volume}.{data_gen.outputFormat}')
            assert True
        else:
            assert False
        end_time = time.time()
        # Check if the clock property returns a string that reflects
        # the execution time
        expected_clock = f":: Time taken: \x1b[31m\
{time.strftime('%X', time.gmtime(end_time - start_time))}\x1b[0m"
        expected_clock = f"{expected_clock}"
        self.assertEqual(data_gen.clock, expected_clock)

    def test_generate_with_conf(self):
        # Create a DataGenerator instance with a configuration file
        data_gen = DataGenerator(volume=100,
                                 file="tests/test_assect/test_data",
                                 conf_file=r'tests/test_assect/test_conf.csv',
                                 format="parquet", choice="m")

        # Call the generateWithConf method
        data_gen.df_mock = pd.DataFrame()
        data_gen.df_mock = data_gen.generateWithConf()
        data_gen.genMockData(data_gen.df_mock)
        df = data_gen.generateWithConf(unique=True)

        # Assert that the returned value is a pd.DataFrame object
        assert isinstance(df, pd.DataFrame)

        # Check that the returned DataFrame has the correct
        # number of rows and columns
        # Replace with the expected shape of the DataFrame
        expected_shape = (100, 18)
        assert df.shape == expected_shape

        # Check that the unique index columns have unique values
        for column, start_number in data_gen.uniqueIndexs:
            assert df[column].nunique() == 100

        # Check that the dependent date range columns have valid dates
        for column, data in data_gen.dependentDateRanges:
            assert pd.to_datetime(df[column], errors='coerce').notnull().all()

        # Check that the composite columns have unique values
        for column, data in data_gen.composites:
            assert df[column].nunique() == 100

    def test_gen_mock_data(self):
        # Create a mock DataFrame
        df = pd.DataFrame({
            "A": [1, 2, 3, 4],
            "B": ["a", "b", "c", "d"],
            "C": [True, False, True, False]
        })

        self.data_gen.n = 100
        mock_df = self.data_gen.genMockData(df)
        # Check if the returned DataFrame has the expected
        # number of rows and columns
        self.assertEqual(mock_df.shape, (100, 3))

        # Check if the returned DataFrame contains only values that are
        # present in the original DataFrame
        for col in df.columns:
            self.assertTrue(mock_df[col].isin(df[col]).all())

    def test_get_by_type(self):
        # Create a mock configuration dictionary
        self.data_gen.conf_dict = {
            "col1": {"name": "Column 1", "type": "string", "values": "abc"},
            "col2": {"name": "Column 2", "type": "number", "values": "123"},
            "col3": {"name": "Column 3", "type": "string", "values": "def"},
            "col4": {"name": "Column 4", "type": "boolean", "values": "true"},
        }

        str_items = self.data_gen.getByType("string")
        num_items = self.data_gen.getByType("number")
        bool_items = self.data_gen.getByType("boolean")

        # Check if the returned list has the expected number of tuples
        self.assertEqual(len(str_items), 2)
        self.assertEqual(len(num_items), 1)
        self.assertEqual(len(bool_items), 1)

        # Check if each tuple contains the expected 'name' and 'values' keys
        self.assertIn(("Column 1", "abc"), str_items)
        self.assertIn(("Column 3", "def"), str_items)
        self.assertIn(("Column 2", "123"), num_items)
        self.assertIn(("Column 4", "true"), bool_items)

    @patch('sdgp.sdgp.DataGenerator.saveInCSV')
    def test_output_csv(self, mock_saveInCSV):
        # Create a DataGenerator instance with output format csv
        data_gen = DataGenerator(volume=10, file="tests/test_data",
                                 conf_file=r'tests/test_assect/test_conf.csv',
                                 format="csv", choice="m")

        # Call the output method and check if the saveInCSV method is called
        data_gen.generateMockData()
        mock_saveInCSV.assert_called_once()

    @patch('sdgp.sdgp.DataGenerator.saveInParquet')
    def test_output_parquet(self, mock_saveInParquet):
        # Create a DataGenerator instance with output format parquet
        data_gen = DataGenerator(volume=10, file="tests/test_data",
                                 conf_file=r'tests/test_assect/test_conf.csv',
                                 format="parquet", choice="m")

        # Call the output method and check if the
        # saveInParquet method is called
        data_gen.generateMockData()
        mock_saveInParquet.assert_called_once()

    @patch('sdgp.sdgp.DataGenerator.generateWithConf')
    @patch('sdgp.sdgp.DataGenerator.genMockData')
    @patch('sdgp.sdgp.DataGenerator.output')
    def test_generate_mock_data(self, mock_output, mock_genMockData,
                                mock_generateWithConf):
        # Create a DataGenerator instance with mock values
        data_gen = DataGenerator(volume=20000, file=self.file,
                                 conf_file=self.conf_file, format=self.format,
                                 choice=self.choice)

        # Call the generateMockData method and check if the corresponding
        # methods are called
        data_gen.generateMockData()
        mock_generateWithConf.assert_called_with(unique=True)
        mock_genMockData.assert_called()
        mock_output.assert_called()

    @patch('sdgp.sdgp.DataGenerator.generateWithConf')
    @patch('sdgp.sdgp.DataGenerator.genMockData')
    @patch('sdgp.sdgp.DataGenerator.editMockDataAndGenerate')
    @patch('sdgp.sdgp.DataGenerator.output')
    def test_edit_mock_data_and_generate(self, mock_output,
                                         mock_editMockDataAndGenerate,
                                         mock_genMockData,
                                         mock_generateWithConf):

        # Create a DataGenerator instance with mock values
        data_gen = DataGenerator(volume=self.volume, file=self.file,
                                 conf_file='tests/test_assect/test_conf.csv',
                                 format=self.format,
                                 choice="e")
        # Call the editMockDataAndGenerate method and check if the
        # corresponding methods are called
        data_gen.editMockDataAndGenerate()
        data_gen.genMockData(
            data_gen.checkFile(r'tests/test_assect/test_data.csv'))
        data_gen.generateWithConf(True)
        data_gen.output()
        mock_editMockDataAndGenerate.assert_called()
        mock_genMockData.assert_called()
        mock_generateWithConf.assert_called()
        mock_output.assert_called()

    @patch('sdgp.sdgp.DataGenerator.genMockData')
    @patch('sdgp.sdgp.DataGenerator.output')
    def test_just_scale_data(self, mock_output, mock_genMockData):
        # Create a DataGenerator instance with mock values
        data_gen = DataGenerator(volume=self.volume,
                                 file=r'tests/test_assect/test_data.csv',
                                 conf_file=None, format=self.format,
                                 choice="g")

        # Call the justScaleData method and check if the corresponding
        # methods are called
        data_gen.justScaleData()
        mock_genMockData.assert_called()
        mock_output.assert_called()

    def test_invalid_choice(self):
        # Create a DataGenerator instance with an invalid choice
        data_gen = DataGenerator(volume=self.volume, file=self.file,
                                 conf_file=None, format=self.format,
                                 choice="x")

        # Call the generateMockData method and check if it raises an exception
        with self.assertRaises(Exception):
            data_gen.generateMockData()

    def test_missing_conf_file(self):
        # Create a DataGenerator instance with a missing configuration file
        with self.assertRaises(SystemExit):
            DataGenerator(volume=self.volume, file=self.file,
                          conf_file="missing.csv",
                          format=self.format, choice="e")
