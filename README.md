## Utilization [Synthetic data generator plus]() Project
For questions on this package contact the package Developer Damodhar Jangam at
## Overview
This project [Synthetic data generator plus]() is a python script that generates mock data based on given configurations. It can also edit and scale existing data to create high volume data. It is useful for testing and prototyping purposes.
## Features
- Generate mock data for different types of configuration items
- Edit the mock data and generate mock data for different types of configuration items
- Configuration rules include generating unique indices, fixed or random dates/times, categorical values, float values within a range, integer values within a range, or constant values.
- Generate high volume data
- Save a DataFrame in CSV and Parquet file formats
## Package Installation
### Install on a Local Machine (optional)
Go through the following sequence:
- Clone repo
- Create a virtual environment and install the package
```bash
PS > python -m venv .venv
PS > .\.venv\Scripts\activate
PS > pip install -r requirements.txt
PS > deactivate # when you need exit
```
### Install on a edge node (optional)
Go through the following sequence:
- Clone repo
- Create a virtual environment and install the package
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ deactivate # when you need exit
```
At that point you're good to go and the package `Synthetic data generater plus` and its module will be
available for use in your virtual environment.
## Usage
To run the script, you need to provide some arguments:
- `-c` or `--choice`: The type of function to select. `m` for mock data, `e` for edit mock data, `g` for generate high volume data.
- `volume`: The size. An integer value that specifies how many rows to generate mock data. Recommended minimum value is more than volume size or more than 1000.
- `format`: The type of format to save the mock data. `csv` for CSV format, `parquet` for Parquet format.
- `csv_file`: The CSV file name. A string value that specifies the name of the CSV file to read if there or to write output.
- `conf_csv_file`: The configuration CSV file name. A string value that specifies the name of the configuration CSV file to read. This argument is required if mode is `e` or `g`.
Example configuration file:

| name          | type               | values                                                  |
| ------------- | ------------------ | ------------------------------------------------------- |
| id1           | uniqueIndex        | 800000000                                               |
| date1         | date               | 2022-10-26 \|%Y-%m-%d                                   |
| time1         | time               | 00:00:00\|23:59:59                                      |
| dateRange1    | dateRange          | 2021-10-10 \| 2022-10-26 \|%Y-%m-%d                     |
| incometime2   | dateRange          | 2021-10-10 \| 2022-10-26 \|%Y-%m-%d %H:%M:%S            |
| outcometime3  | dependentDateRange | incometime2\|1D\|3W\|%Y-%m-%d %H:%M:%S                  |
| model1        | category           | Customers\|Lending\|Web_Lending                         |
| probability1  | floatRange         | 0.001\|1\|3                                             |
| float1        | floatRange         | 0.001\|0.3\|5                                           |
| number1       | intRange           | 10\|25                                                  |
| test1         | constant           | Done                                                    |
| name1         | regexPattern       | ([a-z]{3,10})\, ([a-z]{3,10})                           |
| phone_number  | regexPattern       | (\+[4-9]{2,3})\-([4-9]{5})\-([4-9]{5})                  |
| zip_code      | regexPattern       | ([4-9]{5})                                              |
| email_address | regexPattern       | ([a-zA-Z0-9]{1,10})\@[a-z]{1,5}\.(com\|net\|org\|in)    |
| compositeKey  | composite          | dateRange1 \| model1 \|number1 \|phone_number\|zip_code |

```bash
name,type,values
id1,uniqueIndex,800000000
date1,date,2022-10-26|%Y-%m-%d
time1,time,00:00:00|23:59:59|%H:%M:%S
dateRange1,dateRange,2021-10-10 | 2022-10-26|%Y-%m-%d
incometime2,dateRange,2021-10-10 | 2022-10-26|%Y-%m-%d %H:%M:%S
outcometime3,dependentDateRange,incometime2|1D|3W|%Y-%m-%d %H:%M:%S
model1,category,Customers|Lending|Web_Lending||
probability1,floatRange,0.001|1|3
float1,floatRange,0.001|0.3|5
number1,intRange,10|25
test1,constant,Done
name1,regexPattern,"([a-z]{3,10})\, ([a-z]{3,10})"
phone_number,regexPattern,"(\+[4-9]{2,3})\-([4-9]{5})\-([4-9]{5})"
zip_code,regexPattern,([4-9]{5})
email_address,regexPattern,"([a-zA-Z0-9]{1,10})\@[a-z]{1,5}\.(com|net|org|in)"
compositeKey1,composite,dateRange1|model1|number1|phone_number|zip_code
```
Explanation of above file:
- `uniqueIndex`: This indicates that the `id1` column should contain unique and sequential values, starting from `800000000`.
- `date`: This indicates that the `date1` column should contain a fixed date value (`2022-10-26`) for all rows. `%Y-%m-%d` format is used.
- `time`: This indicates that the `time1` column should contain random time values between `00:00:00` and `23:59:59`.
- `dateRange`: This indicates that the `dateRange1` and `incometime2` columns should contain random date values within the range from `2021-10-10` to `2022-10-26`. The format of the dates in `incometime2` also includes`%Y-%m-%d %H:%M:%S`. format reference given below.
- `dependentDateRange`: This indicates that the `outcometime3` column should contain random duration values within the range from `1D` to `3W` in addition to the `incometime2`.Here `1D` means 1 day and `3W` means 3 weeks. Other compatable inputs are `10S` means 10 seconds, `5m` means 5 minutes, `2h` means 2 hours, `3d` means 3 days, `4W` means 4 weeks. The format of the dates in `outcometime3` also includes`%Y-%m-%d %H:%M:%S`. format reference given below.
- `category`: This indicates that the `model` column should contain random categorical values chosen from the options "Customers", "Lending", and "Web_Lending".
- `floatRange`: This indicates that the `probability1` and `float` columns should contain random float values within a given range. The range for `probability1` is from `0.001` to `1`, with a precision of 3 decimal places. The range for `float` is from `0.001` to `0.3`, with a precision of 5 decimal places.
- `intRange`: This indicates that the `number1` column should contain random integer values within the range from 10 to 25.
- `constant`: This indicates that the `test1` column should contain a constant value (`Done`) for all rows.
- `regexPattern`: This indicates that the `name1` column should contain a fixed pattren range value (`([a-z]{3,10})\, ([a-z]{3,10})`) for all records. The`phone_number` column should contain a fixed length phone number value (`(\+[4-9]{2,3})\-([1-9]{5})\-([1-9]{5})`) for all records. The `zip_code` column should contain a fixed length zip code value (`([4-9]{5})`) for all records. `email_address` column should contain a fixed length email address value (`([a-zA-Z0-9]{1,10})\@[a-z]{1,5}\.(com|net|org|in)`) for all records. For more regex pattren check [here](https://docs.python.org/3/howto/regex.html#simple-patterns) and play around with it.
- `composite`: This indicates that the `compositeKey1` column should contain sha256 hashed value from these combinations: `dateRange1|model1|number1|phone_number|zip_code`
Each row in this CSV file defines a rule for generating or handling data in a specific column of another dataset. The rules include generating unique indices, fixed or random dates/times, categorical values, float values within a range, integer values within a range, or constant values.
datetime formats you can use in the script:
- `%a`: Weekday as locale’s abbreviated name. Example: Mon
- `%A`: Weekday as locale’s full name. Example: Monday
- `%w`: Weekday as a decimal number, where 0 is Sunday and 6 is Saturday. Example: 1
- `%d`: Day of the month as a zero-padded decimal number. Example: 30
- `%b`: Month as locale’s abbreviated name. Example: Sep
- `%B`: Month as locale’s full name. Example: September
- `%m`: Month as a zero-padded decimal number. Example: 09
- `%y`: Year without century as a zero-padded decimal number. Example: 99
- `%Y`: Year with century as a decimal number. Example: 2013
- `%H`: Hour (24-hour clock) as a zero-padded decimal number. Example: 07
- `%I`: Hour (12-hour clock) as a zero-padded decimal number. Example: 07
- `%p`: Locale’s equivalent of either AM or PM. Example: AM
- `%M`: Minute as a zero-padded decimal number. Example: 06
- `%S`: Second as a zero-padded decimal number. Example: 05
To run the script, use the following command:
```
# python main.py -c <choice> <volume> <format> <csv_file> <conf_csv_file>
#
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
```
For example:
```bash
python main.py -c m 50000 csv mock_table conf.csv # Generate 50000 rows of mock data and save as mock_table_50000.csv
python main.py -c e 100000 parquet edit_table.csv conf.csv # Along with given data can edit with conf.csv, generate 100000 recrds and save as edit_table_100000.parquet\n
python main.py -c g 1000000 csv scale.csv # Generate 1000000 rows of mock data by scaling existing data and save as scale_1000000.csv
```
Sample output for `python .\main.py -c m 1000000 csv test .\test_conf.csv `:
![image.png](./confluence/145434.png)
```bash
id1,date1,model1,probability1,float1,number1,test1,time1,dateRange1,incometime2,outcometime3,name1,phone_number,zip_code,email_address,compositeKey1
800000004,2022-10-26,,0.792,0.14948,12,Done,11:34:20,2022-04-07,2022-06-28 21:33:32,2022-07-03 09:41:10,"gkxtawx, pfuf",+65-67845-69497,65957,ji8et6@u.net,c05b0a767331f3176ec3cdf3dee852759a858e30
800000001,2022-10-26,Lending,0.442,0.11305,24,Done,06:01:02,2022-06-18,2022-07-04 01:51:18,2022-07-20 04:31:45,"ttjwjy, zesc",+48-89997-49658,78754,YYChHbaJD@oid.com,ac8759aac34e718dad0ef46c62edb5bff07cb003
800000009,2022-10-26,Lending,0.267,0.17349,17,Done,08:43:08,2022-01-31,2021-12-11 02:33:20,2021-12-19 22:29:15,"vlflyewer, ilj",+564-44495-77467,98785,3mjDBVliLT@ydbpg.com,c068d7d1a8d5e1c6527f84246d8b9dc911b52884
800000003,2022-10-26,,0.565,0.20937,11,Done,02:52:08,2022-04-27,2022-10-25 22:21:19,2022-11-15 16:22:14,"orkilkzh, xozrfwwrtq",+88-95566-65789,68677,Ulq@u.org,d51540c711301c6badc2aad051bb048fd175201b
```
![image.png](./confluence/232516.png)
## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
## Acknowledgments
If you have any questions, feedback, or suggestions, please feel free to contact me at damodhar.jangam@wellsfargo.com. You can also open an issue or submit a pull request on GitHub if you want to contribute to this project.
I hope you find this project useful and interesting. Thank you for reading! 😊
