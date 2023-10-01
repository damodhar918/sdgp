"""Console script for sdgp."""
import argparse
import sys
from colorama import Fore
from .sdgp import DataGenerator

def main():
    """Console script for sdgp."""
    # Create a parser object with a description of your script
    parser = argparse.ArgumentParser(
        description="""This is a script that generates mock data.\n
\t1. main.py -c m 50000 csv mock_table conf.csv # Generate 50000 rows of mock data and save as mock_table_50000.csv\n
\t2. main.py -c e 100000 parquet edit_table.csv conf.csv # Along with given data can edit with conf.csv, generate 100000 recrds and save as edit_table_100000.parquet\n
\t3. main.py -c g 1000000 csv scale.csv # Generate 1000000 rows of mock data by scaling existing data and save as scale_1000000.csv\n
""")
    # Add arguments to the parser object
    parser.add_argument("-c", "--choice", type=str, choices=[
                        'm', 'e', 'g'], help="The type of function to select. m for mock data, e for edit mock data, g for generate high volume data.")
    # Add a volume argument to the parser object
    parser.add_argument(
        "volume", type=int, help="The size. An integer value that specifies how many rows to generate mock data. Recommended minimum value is more than volume size or more than 1000.")
    parser.add_argument(
        "format", type=str, choices=['csv', 'parquet'], help="The type of format to save the mock data. csv for CSV format, parquet for Parquet format.")
    parser.add_argument("csv_file", type=str,
                        help="The CSV file name. A string value that specifies the name of the CSV file to read or write.")
    # Change this line to make conf_csv_file optional for some modes
    parser.add_argument("conf_csv_file", type=str, default=None, nargs='?',
                        help="The configuration CSV file name. A string value that specifies the name of the configuration CSV file to read. This argument is required if mode is e or g.")
    # Parse the arguments
    args = parser.parse_args()
    # Change the mode variable to choice
    choice = args.choice
    LENGTH = 122
    print(Fore.CYAN + '#'*LENGTH+Fore.WHITE)
    # Pass the arguments to your class constructor as parameters
    data_gen = DataGenerator(volume=args.volume, file=args.csv_file.strip('.\\'),
                             conf_file=args.conf_csv_file.strip('.\\'),  format=args.format, choice=choice)

    def suggestion():
        print(Fore.CYAN + '#'*LENGTH+Fore.WHITE)
        print(Fore.CYAN + '#'+Fore.WHITE, end='')
        print(
            " If you have any suggestion or any question, please contact Damodhar Jangam                                             ",
            sep=Fore.CYAN + "#\n# " + Fore.WHITE,
            end='')
        print(Fore.CYAN + '#'+Fore.WHITE,)
        print(Fore.CYAN + '#'*LENGTH+Fore.WHITE)
    # Use the choice argument to select a function from your class
    if choice == 'm' and args.conf_csv_file:
        data_gen.generateMockData()
        suggestion()
    elif choice == 'e' and args.conf_csv_file:
        data_gen.editMockDataAndGenerate()
        suggestion()
    elif choice == 'g':
        data_gen.justScaleData()
        suggestion()
    else:
        print(" Invalid choice or configuration file not found!\n try: main.py -h for help")
        print(Fore.CYAN + '#'*LENGTH+Fore.WHITE)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
