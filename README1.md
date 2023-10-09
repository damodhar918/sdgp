## Utilization of Beeline Ingestion with Synthetic Data Generator Plus Project

For questions on this package contact the package Developer Damodhar Jangam or Vyasa Koundinya, Lanka.

## Overview
This project is an extension of the Synthetic Data Generator Plus project which includes Beeline Ingestion of generated data into Hadoop. In addition to generating synthetic data, this package allows user to ingest the generated data into Beeline table by leveraging JDBC connection to Hive server 2.

## Features
- Build Beeline Ingestion connection to Hadoop cluster.
- Generate mock data for different types of configuration items.
- Edit the mock data and generate mock data for different types of configuration items.
- Configuration rules include generating unique indices, fixed or random dates/times, categorical values, float values within a range, integer values within a range, or constant values.
- Generate high volume data.
- Save a DataFrame in CSV and Parquet file formats.
- Ingest mock data into Beeline table using the established connection.

## Package Installation

### Install on a Local Machine (optional)
Go through the following sequence:

- Clone repo.
- Create a virtual environment and install the package:

```
PS > python -m venv .venv
PS > .\.venv\Scripts\activate
PS > pip install -r requirements.txt
PS > deactivate # when you need exit
```

### Install on an edge node (optional)
Go through the following sequence:

- Clone repo.
- Create a virtual environment and install the package:

```
$ python3 -m venv .venv
$ source env/bin/activate
$ pip install -r requirements.txt
$ deactivate # when you need exit
```

At this point, you're good to go and the package and its modules will be available for use in your virtual environment.

## Usage

Before consuming this package make sure you have established JDBC connection to the Hadoop cluster.

To run the script, you need to provide some arguments:

- `-c` or `--choice`: The type of function to select. `m` for mock data, `e` for edit mock data, `g` for generate high volume data and `i` for ingestion of mock data into Hive Table after generation.
- `volume`: The size. An integer value that specifies how many rows to generate mock data. Recommended minimum value is more than volume size or more than 1000.
- `format`: The type of format to save the mock data. `csv` for CSV format, `parquet` for Parquet format.
- `csv_file`: The CSV file name. A string value that specifies the name of the CSV file to read if there or to write output.
- `conf_csv_file`: The configuration CSV file name. A string value that specifies the name of the configuration CSV file to read. This argument is required if mode is `e`, `g` or `i`.
- `hive_table`: The name of the hive table to ingest data. This argument is required for `i` mode.

The configuration parameters can be stored in a JSON-format properties file, like `properties.json`, as follows:

```
{
  "table": "XXX",
  "schema": "XXX",
  "partitionColumns": ["col1", "col2"],
  "hive1": "jdbc:XXX",
  "beelinePath": "/path/to/beeline"
}
```

To generate the data and ingest it into Beeline table using the configuration file:

```
import json

with open('properties.json', 'r') as f:
    props = json.load(f)

beeline_ingest = Connection(props["hive1""], props["beelinePath"])
beeline_ingest.run(["-c", "i", "10000", "csv", "mock_data.csv", "config.csv", props["table"]])
```

Sample output for `python .\sdgp -c i 10000 csv mock_table .\test_conf.csv test_hive_table`: Data will be generated in `mock_table.csv` and ingested in `test_hive_table`.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Acknowledgments

If you have any questions, feedback, or suggestions, please feel free to contact me at lvyasakoundinya@deloitte.com, jdamodhar@deloitte.com. You can also open an issue or submit a pull request on GitHub if you want to contribute to this project.
I hope you find this project useful and interesting. Thank you for reading! 😊
