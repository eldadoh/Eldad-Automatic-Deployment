import csv
from pandas_utils import save_df_as_csv
import pandas as pd
import numpy as np 
import os
import glob
import shutil 

def sort_annotations_df_by_class(df : pd.DataFrame,dir_path : str) -> pd.DataFrame:
    
    df = df[['image_name','annotation','x','y','width','height']]
    df = df.sort_values('annotation')
    df['full_img_path'] = dir_path +'/' + df['image_name']
    df = df[['full_img_path','annotation','x','y','width','height']]
    
    return df 

def handle_single_csv_dir_func(dir_path : str, param_dict : dict ,verbose : bool = True) -> pd.DataFrame:

    annotation_file_name_const = param_dict['annotation_file_name_const']
    annotation_file_path = os.path.join(dir_path,annotation_file_name_const)
    
    df = pd.read_csv(annotation_file_path)
    
    df_sorted_by_class = sort_annotations_df_by_class(df,dir_path)

    if verbose : 
        print ('\nDone handling single dir from (csv-format) ===> ' + f'{os.path.dirname(annotation_file_path)}')

    return df_sorted_by_class 

