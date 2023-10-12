
import io
import os
import sys
from unittest.mock import patch
from sdgp.cli import main


def test_main_mock_data():
    mock_file_name = r'tests/mock_table.csv'
    mock_file_outfile = mock_file_name.split('.csv')[0] \
        if mock_file_name.strip().endswith('.csv') else mock_file_name
    conf_file = r'tests/test_assect/test_conf.csv'
    file_format = 'csv'
    records = str(500)
    mode = 'm'
    with patch.object(sys, 'argv', ['sdgp', '-c', 'm', records, file_format,
                                    mock_file_name,
                                    conf_file]):
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            main()
            assert f'Fetched the file {conf_file}! Time taken:' \
                in fake_output.getvalue()
            assert f'File has been saved as {mock_file_outfile}\
_{mode}_{records}.{file_format}! Time taken: ' in fake_output.getvalue()
            if os.path.exists(f'{mock_file_outfile}\
_{mode}_{records}.{file_format}'):
                os.remove(f'{mock_file_outfile}\
_{mode}_{records}.{file_format}')
                assert True
            else:
                assert False


def test_main_mock_data_with_large_number_of_records():
    mock_file_name = r'tests/mock_table.csv'
    mock_file_outfile = mock_file_name.split('.csv')[0] \
        if mock_file_name.strip().endswith('.csv') else mock_file_name
    conf_file = r'tests/test_assect/test_conf.csv'
    file_format = 'csv'
    mode = 'm'
    records = str(1500)
    with patch.object(sys, 'argv', ['sdgp', '-c', 'm', records, file_format,
                                    mock_file_name,
                                    conf_file]):
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            main()
            assert f'File has been saved as {mock_file_outfile}\
_{mode}_{records}.{file_format}! Time taken: ' in fake_output.getvalue()
            if os.path.exists(f'{mock_file_outfile}\
_{mode}_{records}.{file_format}'):
                os.remove(f'{mock_file_outfile}\
_{mode}_{records}.{file_format}')
                assert True
            else:
                assert False


def test_main_mock_data_with_edit_csv_to_parquet():
    mock_file_name = r'tests/test_assect/test_data.csv'
    mock_file_outfile = mock_file_name.split('.csv')[0] \
        if mock_file_name.strip().endswith('.csv') else mock_file_name
    conf_file = r'tests/test_assect/test_conf.csv'
    file_format = 'csv'
    mode = 'm'
    records = str(1500)
    with patch.object(sys, 'argv', ['sdgp', '-c', mode, records, file_format,
                                    mock_file_name,
                                    conf_file]):
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            main()
            assert f'File has been saved as {mock_file_outfile}\
_{mode}_{records}.{file_format}! Time taken: ' in fake_output.getvalue()
            if os.path.exists(f'{mock_file_outfile}\
_{mode}_{records}.{file_format}'):
                os.remove(f'{mock_file_outfile}\
_{mode}_{records}.{file_format}')
                assert True
            else:
                assert False


def test_main_mock_data_scale_with_duplicates():
    mock_file_name = r'tests/test_assect/test_data.csv'
    mock_file_outfile = mock_file_name.split('.csv')[0] \
        if mock_file_name.strip().endswith('.csv') else mock_file_name
    conf_file = r'tests/test_assect/test_conf.csv'
    file_format = 'csv'
    mode = 'g'
    records = str(4000)
    with patch.object(sys, 'argv', ['sdgp', '-c', mode, records, file_format,
                                    mock_file_name,
                                    conf_file]):
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            main()
            assert f'File has been saved as {mock_file_outfile}\
_{mode}_{records}.{file_format}! Time taken: ' in fake_output.getvalue()
            if os.path.exists(f'{mock_file_outfile}\
_{mode}_{records}.{file_format}'):
                os.remove(f'{mock_file_outfile}\
_{mode}_{records}.{file_format}')
                assert True
            else:
                assert False
