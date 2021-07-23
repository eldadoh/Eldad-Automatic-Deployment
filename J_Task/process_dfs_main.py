import os
import glob
import csv
import pandas as pd 
import shutil 

def load_df_from_csv(csv_file_path:str, sep = ',') -> pd.DataFrame :

    df = pd.read_csv(csv_file_path,sep)

    return df 

def get_duplicates_from_df (df,key,Output_path,NAME_OF_DF) : 
    
    df = df[df.duplicated(f'{key}',keep=False)]
    df = df.drop(columns=['Unnamed: 0'])
    df = df.sort_values(f'{key}')
    df.to_csv(f'{Output_path}/duplicates_in_'+f'{NAME_OF_DF}' +'.csv')


def main(): 

    IMAGES_DIRS__CSV_PATH = 'Outputs/Raw_df/images_dirs_df.csv'
    PRODUCT_LIST__CSV_PATH = 'Outputs/Raw_df/Product_list_df.csv'
    THUMNBAILS_DIR_CSV_PATH = 'Outputs/Raw_df/Thumbnails_df.csv' 

    DUPLICATES_DIR_OUTPUT_PATH = 'Outputs/duplicates_df'


    images_dir_df = load_df_from_csv(IMAGES_DIRS__CSV_PATH,sep ='\t')
    product_list_df = load_df_from_csv(PRODUCT_LIST__CSV_PATH,sep ='\t')
    thumbnails_df = load_df_from_csv(THUMNBAILS_DIR_CSV_PATH,sep ='\t')

    get_duplicates_from_df(product_list_df,'UPC',DUPLICATES_DIR_OUTPUT_PATH,NAME_OF_DF = 'product_list')
    get_duplicates_from_df(thumbnails_df,'UPC',DUPLICATES_DIR_OUTPUT_PATH,NAME_OF_DF = 'thumbnails_df')

if __name__ == "__main__":
    
    main()
