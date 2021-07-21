import pandas as pd
import numpy as np 
import os
import glob
import shutil 
import json
import csv 
from handle_single_csv_dir import handle_single_csv_dir_func
from pandas_utils import save_df_as_csv
# from handle_single_json_dir import handle_single_json_dir_func

"""
This file task is only to aggeregate all the csv&json annotation files data
analysis of the this aggeregated (clear df) is on other file
"""

def handle_all_csv_dirs(main_csv_dir_path : str,param_dict : dict , verbose : bool = True , save : bool = False):
    
    small_dfs = []
    
    for dir_name in os.listdir(main_csv_dir_path):
        single_dir_path = os.path.join(main_csv_dir_path,dir_name)
        df = handle_single_csv_dir_func(single_dir_path,param_dict)
        small_dfs.append(df)
    
    large_df = pd.concat(small_dfs, ignore_index=True) 
    
    if verbose : 
        print(f'\nDone handling main_csv_dir_path : {main_csv_dir_path}\n')
    
    if save:
        save_df_as_csv(large_df,'Output/clear_df.csv')

def main(): 

    MAIN_ANNOTATIONS_DIR_PATH_CSV = 'Data/annotations/csv'
    MAIN_ANNOTATIONS_DIR_PATH_JSON = 'Data/annotations/json'

    PARAM_DICT ={'annotation_file_name_const' : 'annotations.csv'}

    handle_all_csv_dirs(MAIN_ANNOTATIONS_DIR_PATH_CSV,param_dict=PARAM_DICT,save=True)
        
if __name__ == '__main__':
    main()