import xlrd
import csv
import os 
import pandas as pd


def xlsx_to_csv(file_path,sheet_name='Sheet1'):

    file_name = os.path.basename(file_path)
    data_xls = pd.read_excel(f'{file_path}', f'{sheet_name}', dtype=str, index_col=None)
    data_xls.to_csv(f'Output/{file_name}.csv', encoding='utf-8', index=False)


def main():

    file_path = 'Data/Example-Mapping-Files/doralon_mixed-rms-mana-hama-categories_annotation-to-class.xlsx'

    xlsx_to_csv(file_path)

if __name__ == "__main__": 
    main()