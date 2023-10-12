"""Main module."""
####################################################################################################################################################
# Script Name      : sdgp (Synthetic Data Generater + )
# Script Details   : This is a script that generates mock data.
#
# usage            : sdgp [-h] [-c {m,e,g}] volume {csv,parquet} csv_file [conf_csv_file]
#
#   This is a script that generates mock data.
#          1. sdgp -c m 50000 csv mock_table conf.csv # Generate 50000 rows of mock data and save as mock_table_50000.csv
#          2. sdgp -c e 100000 parquet edit_table.csv conf.csv # Along with given data can edit with conf.csv, generate 100000 recrds and save as edit_table_100000.parquet
#          3. sdgp -c g 1000000 csv scale.csv # Generate 1000000  # rows of mock data by scaling existing data and save as scale_1000000.csv
# positional arguments:
#   volume                The size. An integer value that specifies how many rows to generate mock data. Recommended
#                         minimum value is more than volume size or more than 1000.
#   {csv,parquet}         The type of format to save the mock data. csv for CSV format, parquet for Parquet format.
#   csv_file              The CSV file name. A string value that specifies the name of the CSV file to read or write.
#   conf_csv_file         The configuration CSV file name. A string value that specifies the name of the configuration
#                         CSV file to read. This argument is required if mode is e or g.
# options:
#   -h, --help            show this help message and exit
#   -c {m,e,g}, --choice {m,e,g}
#                         The type of function to select. m for mock data, e for edit mock data, g for generate high
#                         volume data.
#
# ================================================================================================================================================
#    Date of Change                         Developer                                                                   Change Log
# ==================================================================================================================================================
#     2023-09-06                            Damodhar Jangam                                                Initial Creation
####################################################################################################################################################
import pandas as pd
import numpy as np
import hashlib
import random
import time
from datetime import datetime, timedelta
import pyarrow as pa
import pyarrow.parquet as pq
import sys
import exrex


class DataGenerator:
    """
    The 'DataGenerator' class is used to generate and manipulate data based on
    given configurations. It has methods to convert a date string into a
    pandas datetime object, generate random dates within a given range,
    save a DataFrame in CSV and Parquet file formats,
    create a mock DataFrame by randomly selecting values from the
    original DataFrame, retrieve configuration items by type, split a
    string by pipe character,
    generate mock data for different types of configuration items,
    and edit the mock data. The class also has placeholder methods for
    generating high volume data and editing the mock data.
    Args:
            volume (int): The number of rows to generate for the mock data.
            file (str): The name of the CSV file to generate / sameple file to
            edit and generate.
            conf_file (str): The name of the configuration CSV file to read.
            format (str): The format to save the mock data
            (either "csv" or "parquet").
            choice (str): The type of function to select
            ("m" for mock data, "e" for edit mock data,
            "g" for generate high volume data).
    """

    def __init__(self, volume: int, file: str, conf_file: str,
                 format: str, choice: str):
        """
        Constructor for the DataGenerator class.
        Args:
            volume (int): The number of rows to generate for the mock data.
            file (str): The name of the CSV file to generate /
            sameple file to edit and generate.
            conf_file (str): The name of the configuration CSV file to read.
            format (str): The format to save the mock data
            (either "csv" or "parquet").
            choice (str): The type of function to select
            ("m" for mock data, "e" for edit mock data,
            "g" for generate high volume data).
        """
        self.n = int(volume)  # Number of rows to generate
        self.volume = int(volume)  # Number of rows to volume
        self.file = file.split('.csv')[0] \
            if file.strip().endswith('.csv') else file  # File name to generate
        self.csv_file_path = file.strip()  # to read CSV file path
        self.start_time = time.time()
        self.outputFormat = format
        self.choice = choice
        if conf_file:
            self.conf_file_path = conf_file.strip()
            self.conf_df = self.checkFile(self.conf_file_path)
            self.conf_dict = self.conf_df.to_dict(
                orient='index')  # Configuration dictionary

    @property
    def clock(self):
        return f"; Time taken: \
{time.strftime('%X', time.gmtime(time.time() - self.start_time))}"

    def checkDate(self, date):
        """
        Convert a date string into a pandas datetime object.
        Args:
            date (str): A string representing a date in
            the format "YYYY-MM-DD".
        Returns:
            pd.Timestamp: A pandas datetime object representing the input date.
        Example Usage:
            date = "2022-01-01"
            result = check_date(date)
            print(result)
            """
        try:
            return pd.to_datetime(date)
        except Exception as e:
            print(e)
            pass

    def checkFile(self, path) -> pd.DataFrame:
        try:
            df = pd.read_csv(path).rename(columns=lambda x: x.split(".")[-1])
            print(f"Fetched the file {path}!", self.clock.strip(" ;"))
            return df
        except Exception as e:
            raise SystemExit(e)


    def generateDates(self, s, e, format) -> list:
        """
        Generate random dates within a given range.
        Args:
            s (str): Start date in the format "YYYY-MM-DD".
            e (str): End date in the format "YYYY-MM-DD".
        Returns:
            list: List of datetime objects representing the generated dates.
        """
        start = self.checkDate(s)
        end = self.checkDate(e)
        self.checkFormat(format)
        if start > end:
            raise ValueError(
                "Start date must be before end date. (start date < end date)")
        dates = []
        for i in range(self.n):
            date = start + (end - start) * random.random()
            dates.append(date.strftime(str(format)))
        return dates

    def saveInCSV(self):
        """
        Save a DataFrame in CSV format.
        Args:
            df (pd.DataFrame): DataFrame to save.
            file_name (str): File name for the CSV file.
        """
        df = self.df_mock.sample(self.volume).drop_duplicates()
        self.mock_file_csv_path = f"{self.file}\
_{self.choice}_{self.volume}.csv"
        df.to_csv(self.mock_file_csv_path, index=False, header=True)
        print(
            f"File has been saved as { self.mock_file_csv_path}!",
            self.clock.strip(" ;"))

    def saveInParquet(self):
        """
        Save a DataFrame in Parquet format.
        Args:
            df (pd.DataFrame): DataFrame to save.
            file_name (str): File name for the Parquet file.
        """
        df = self.df_mock.sample(self.volume).drop_duplicates()
        self.mock_file_parquet_path = f"{self.file}\
_{self.choice}_{self.volume}.parquet"
        table = pa.Table.from_pandas(df, preserve_index=False)
        pq.write_table(table,  self.mock_file_parquet_path,
                       compression="snappy")
        print(
            f"File has been saved as \
{ self.mock_file_parquet_path}!", self.clock.strip(" ;"))

    def genMockData(self, df) -> pd.DataFrame:
        """
        Create a mock DataFrame by randomly selecting values
        from the original DataFrame.
        Args:
            df (pd.DataFrame): Original DataFrame.
        Returns:
            pd.DataFrame: Mock DataFrame.
        """
        self.columns = df.columns
        self.df_mock = pd.concat(
            [df.apply(lambda a: a.sample(frac=1).values)
             for _ in range(int(self.n/df.shape[0]))],
            ignore_index=True,
        )
        return self.df_mock

    def splitByPipe(self, data):
        """
        Splits a string by pipe character and returns a list of strings.
        Args:
            data (str): The string to split.
        Returns:
            list: A list of strings after splitting by pipe character.
        """
        return [*map(str.strip, data.split("|"))]

    def getByType(self, type) -> list:
        """
        Retrieves the name and values of configuration items that match
        a given type from the configuration dictionary.
        Args:
            type (str): The type of configuration items to retrieve.
        Returns:
            list: A list of tuples, where each tuple contains the 'name' and
            'values' of a configuration item that matches the given type.
        """
        return [(item.get('name').strip(), item.get('values').strip()) for
                item in self.conf_dict.values()
                if item.get('type').strip() == type]

    def checkDuration(self, start_duration, end_duration):
        """
        Check if the start date is before the end date.

        Args:
            start_duration (str): A string representing the start duration in
            the format "1D", "1W", etc.
            end_duration (str): A string representing the end duration in the
            format "1D", "1W", etc.

        Returns:
            bool: True if the start date is before the end date,
            otherwise False.

        Raises:
            ValueError: If the start date is after the end date.
        """

        if pd.to_timedelta(start_duration).total_seconds() > \
                pd.to_timedelta(end_duration).total_seconds():
            raise ValueError(
                "Start date must be before end date. \
(start duration < end duration) e.g. 1D < 1W will \
genterate random date between next (1) day to next \
(1) week from start date")
        return True

    def checkFormat(self, format):
        """
        Check if a date format string is valid.

        Args:
            date_format (str): A string representing a date format in the
            format "%Y-%m-%d %H:%M:%S".

        Returns:
            bool: True if the date format is valid, otherwise False.

        Raises:
            ValueError: If the date format is invalid.
        """
        try:
            return pd.Timestamp(datetime.now().strftime(format))
        except ValueError:
            raise ValueError(
                f"Invalid date format {format}.",
                "The format like '%Y-%m-%d %H:%M:%S',",
                "e.g. '2023-10-11 12:48:14'.")

    def addRandomDuration(self, start_date, so, eo, format):
        random_duration = pd.to_timedelta(
            random.uniform(
                pd.to_timedelta(so).total_seconds(),
                pd.to_timedelta(eo).total_seconds()),
            unit='s')
        return (start_date + random_duration).strftime(format)

    def generateWithConf(self, unique=False) -> pd.DataFrame:
        """
        Generates mock data for different types of configuration items and
        assigns them to columns in the mock DataFrame.
        Returns:
            pd.DataFrame: The mock DataFrame with generated data.
        """
        if unique:
            # df = pd.DataFrame()
            for column, start_number in self.uniqueIndexs:
                start_number = int(start_number)
                self.df_mock[column] = np.arange(
                    start_number, start_number + self.n)
            for column, data in self.dependentDateRanges:
                preDate, so, eo, format = self.splitByPipe(data)
                if self.checkDuration(so, eo) and self.checkFormat(format):
                    self.df_mock[column] = pd.to_datetime(
                        self.df_mock[preDate]).apply(
                            lambda x: self.addRandomDuration(
                                x, so, eo, format))
            for column, data in self.composites:
                keys = self.splitByPipe(data)
                self.df_mock[column] = self.df_mock[keys].astype('str')\
                    .sum(1).apply(lambda x: hashlib.sha1(
                        x.encode()).hexdigest())
            return self.df_mock
        self.uniqueIndexs = self.getByType("uniqueIndex")
        self.dateRanges = self.getByType("dateRange")
        self.dates = self.getByType("date")
        self.categories = self.getByType("category")
        self.constants = self.getByType("constant")
        self.floatRanges = self.getByType("floatRange")
        self.intRanges = self.getByType("intRange")
        self.constants = self.getByType("constant")
        self.times = self.getByType("time")
        self.dependentDateRanges = self.getByType("dependentDateRange")
        self.composites = self.getByType("composite")
        self.regexPatterns = self.getByType("regexPattern")
        for column, start_number in self.uniqueIndexs:
            start_number = int(start_number)
            self.df_mock[column] = np.arange(
                start_number, start_number + self.n)
        for column, date in self.dates:
            date, format = self.splitByPipe(date)
            self.df_mock[column] = pd.to_datetime(date).strftime(format)
        for column, data in self.categories:
            suffle_data = self.splitByPipe(data)
            self.df_mock[column] = np.random.choice(suffle_data, self.n)
        for column, data in self.floatRanges:
            s, e, precision = [*map(float, self.splitByPipe(data))]
            self.df_mock[column] = np.round(
                np.random.uniform(s, e, self.n), int(precision))
        for column, data in self.intRanges:
            s, e = [*map(int, self.splitByPipe(data))]
            self.df_mock[column] = np.random.randint(s, e, self.n)
        for column, data in self.constants:
            self.df_mock[column] = data
        for column, data in self.times:
            s, e, format = self.splitByPipe(data)
            random_dates = [datetime.now() + timedelta(
                hours=random.randint(0, 24),
                minutes=random.randint(0, 60),
                seconds=random.randint(0, 60)) for _ in range(self.n)]
            self.df_mock[column] = [pd.to_datetime(
                date).strftime(format) for date in random_dates]
        for column, data in self.dateRanges:
            s, e, format = self.splitByPipe(data)
            self.df_mock[column] = self.generateDates(s, e, format)
        for column, data in self.dependentDateRanges:
            preDate, so, eo, format = self.splitByPipe(data)
            if self.checkDuration(so, eo) and self.checkFormat(format):
                self.df_mock[column] = pd.to_datetime(
                    self.df_mock[preDate]).apply(
                    lambda x: self.addRandomDuration(x, so, eo, format))
        for column, data in self.regexPatterns:
            self.df_mock[column] = self.df_mock.iloc[:, 0].apply(
                lambda x: exrex.getone(data))
        for column, data in self.composites:
            keys = self.splitByPipe(data)
            self.df_mock[column] = self.df_mock[keys].astype('str')\
                .sum(1).apply(lambda x: hashlib.sha1(x.encode()).hexdigest())
        return self.df_mock

    def output(self):
        """
        Checks the output format and calls the corresponding
        method to save the generated data.
        """
        if self.outputFormat == "csv":
            self.saveInCSV()
        elif self.outputFormat == "parquet":
            self.saveInParquet()

    def generateMockData(self):
        """
        Generates mock data based on the given configuration and saves it.
        """
        self.df_mock = pd.DataFrame()
        if self.volume > 10000:
            print("Generated data...",
                  self.clock.strip(" ;"))
            self.df_mock = self.generateWithConf()
            self.genMockData(self.df_mock)
            self.generateWithConf(unique=True)
        else:
            self.df_mock = self.generateWithConf()
        self.output()

    def editMockDataAndGenerate(self):
        """
        Reads a CSV file, generates mock data based
        on the existing data, edit
        and saves it.
        """
        df = self.checkFile(self.csv_file_path)
        print("Generated data...", self.clock.strip(" ;"))
        self.genMockData(df)
        self.generateWithConf()
        self.output()

    def justScaleData(self):
        """
        Reads a CSV file, generates mock data based
        on the existing data, and saves it.
        """
        df = self.checkFile(self.csv_file_path)
        print("Generated data...", self.clock.strip(" ;"))
        self.genMockData(df)
        self.output()
