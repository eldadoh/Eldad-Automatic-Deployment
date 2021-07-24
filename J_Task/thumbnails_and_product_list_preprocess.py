import os
import glob
import csv
from typing import List
from numpy import concatenate, nan
import pandas as pd 
import shutil
import numpy as np


def load_df_from_csv(csv_file_path:str, sep = '\t') -> pd.DataFrame :

    df = pd.read_csv(csv_file_path,sep)

    return df 

def create_dir_with_override(dir_path : str ) -> None :
    try : 
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)
    except Exception as e : 
        print(e)
        print('Could not create the desired dir with the corersponding dir path : \n' + f'{dir_path}')

def find_intersection_of_3(set1 : set,set2 : set ,set3 : set ): 

    return set.intersection(set1, set2, set3)

def create_fixed_thumbnails_names_dir(THUMBNAILS_DIR_PATH : str,OUTPUT_PATH : str ):

    thumbnailes_upc_list = []

    NEW_THUMBNAILS_DIR_PATH  = os.path.join(OUTPUT_PATH , 'Thumbnails_Updated')
    
    create_dir_with_override(NEW_THUMBNAILS_DIR_PATH)

    for img_path in glob.glob(f'{THUMBNAILS_DIR_PATH}/*.png'):

        fixed_name = os.path.basename(img_path)[:-len('.png')]

        if fixed_name.endswith('.1') : 
            
            fixed_name = fixed_name[:-len("abc")] # according to J's instructions 
            fixed_name = fixed_name.lstrip("0")

            thumbnailes_upc_list.append(fixed_name)

            img_new_name_path = os.path.join(NEW_THUMBNAILS_DIR_PATH, fixed_name + '.png')

            shutil.copy(img_path , img_new_name_path)

    return NEW_THUMBNAILS_DIR_PATH, thumbnailes_upc_list

def create_raw_df_PL_and_Thumbnails(PRODUCT_LIST_PATH,thumbnailes_upc_list : list ,OUTPUT_PATH : str):

    product_list_df = load_df_from_csv(PRODUCT_LIST_PATH,sep =',')
    product_list_df = product_list_df[['UPC','2 - CATEGORY','2 - SUB-CATEGORY']]
    product_list_df.columns = ['UPC','CATEGORY','SUB_CATEGORY']
    product_list_df.to_csv('Outputs/Raw_df/Product_list_df.csv',sep ='\t')

    thumbnails_df = pd.DataFrame(thumbnailes_upc_list,columns=["UPC"])
    thumbnails_df.to_csv('Outputs/Raw_df/Thumbnails_df.csv',sep ='\t')


def main(): 

    THUMBNAILS_DIR_PATH = 'Data/Thumbnails'
    PRODUCT_LIST_PATH = 'Data/Full_Product_List.csv'
    OUTPUT_PATH = 'Outputs'

    NEW_THUMBNAILS_DIR_PATH,thumbnailes_upc_list = create_fixed_thumbnails_names_dir(THUMBNAILS_DIR_PATH,OUTPUT_PATH)

    create_raw_df_PL_and_Thumbnails(PRODUCT_LIST_PATH,thumbnailes_upc_list,OUTPUT_PATH) 
    
if __name__ == "__main__":
    
    main()
