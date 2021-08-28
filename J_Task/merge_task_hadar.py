import pandas as pd 
import os,glob

def load_df_from_csv(csv_file_path:str) -> pd.DataFrame :

    df = pd.read_csv(csv_file_path,sep='\t')
    # df = pd.read_csv(csv_file_path,sep=',')
    
    return df 

def load_df_from_xl(file_name,sheet_name = None):
    
    xl_file = pd.ExcelFile(file_name)

    dfs = {sheet_name: xl_file.parse(sheet_name) 
          for sheet_name in xl_file.sheet_names}

    if sheet_name:
          
          return dfs[f'{sheet_name}']

    return dfs 



def main():

    DF_ALL_TIME_PL_PATH = 'Data/merge-task-Hadar/big_all-time_df_PL.xlsx'
    IN_HOUSE_PL_PATH = 'Data/merge-task-Hadar/in-house-PL.tsv'
    df_all_time_PL = load_df_from_xl(DF_ALL_TIME_PL_PATH)
    in_house_pl = load_df_from_csv(IN_HOUSE_PL_PATH)






if __name__ == "__main__":
    
    main()
