import os
import glob
import csv
from typing import List
from numpy import concatenate, nan
import pandas as pd 
import shutil
import numpy as np
from src.pandas_utils import pandas_exp_dataset 

def create_dir_with_override(dir_path : str ) -> None :
    try : 
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)
    except Exception as e : 
        print(e)
        print('Could not create the desired dir with the corersponding dir path : \n' + f'{dir_path}')

def load_df_from_csv(csv_file_path:str, sep = '\t') -> pd.DataFrame :

    df = pd.read_csv(csv_file_path,sep)

    return df 

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

def fetch_thumbnails_and_product_list_data(NEW_THUMBNAILS_DIR_PATH : str,thumbnailes_upc_list : list ,OUTPUT_PATH : str , PRODUCT_LIST_PATH : str ) -> csv : 

######################################################################################################################################################################

    upc_thumbnails_df = pd.DataFrame(thumbnailes_upc_list,columns=["UPC"])
    upc_thumbnails_df_unique = upc_thumbnails_df['UPC'].unique() # 611 
    upc_thumbnails_set = set(upc_thumbnails_df_unique)
    upc_thumbnails_df_unique_df = pd.DataFrame(upc_thumbnails_df['UPC'].unique()) # 611
    upc_thumbnails_df_unique_df.columns = ['UPC']
    upc_thumbnails_df_unique_df = upc_thumbnails_df_unique_df['UPC'].astype(str)

    # upc_thumbnails_df = pd.DataFrame(thumbnailes_upc_list,columns=["UPC"])
    product_list_df = load_df_from_csv(PRODUCT_LIST_PATH,sep =',')
    upc_product_list_df = product_list_df[['UPC','2 - CATEGORY','2 - SUB-CATEGORY']]
    # duplicates_in_product_list = upc_product_list_df[upc_product_list_df.duplicated(keep=False)]
    # duplicates_in_product_list.to_csv('Outputs/Final/duplicates_in_product_list.csv')
    upc_product_list_df_unique = product_list_df['UPC'].unique()

    upc_product_list_set = set(upc_product_list_df_unique) #677 , 668 unique() , 9 duplicates
    upc_product_list_set = {str(num) for num in upc_product_list_df_unique} 

    upc_product_list_df_unique_df = pd.DataFrame(product_list_df['UPC'].unique())
    upc_product_list_df_unique_df.columns = ['UPC']
    upc_product_list_df_unique_df = upc_product_list_df_unique_df['UPC'].astype(str)

    intersection_of_thumnbails_and_product_list = set.intersection(upc_thumbnails_set, upc_product_list_set)

######################################################################################################################################################################
    #find intersection - way2 

    upc_thumbnails_df_unique_df = pd.DataFrame(upc_thumbnails_df_unique_df)
    upc_product_list_df_unique_df = pd.DataFrame(upc_product_list_df_unique_df)

    upc_thumbnails_df_unique_df.merge(upc_product_list_df_unique_df) #intersection only == same rows 

######################################################################################################################################################################
    
    upc_thumbnails_df_unique_df['FROM'] = 'THUMNBAILS'
    upc_product_list_df_unique_df['FROM'] = 'PRODUCT_LIST'

    concatenated_by_rows = pd.concat([ upc_thumbnails_df_unique_df, upc_product_list_df_unique_df], axis = 0)
    
    # first is thumbnails , last is product list 
    concatenated_rows_save_thumbnail = concatenated_by_rows.drop_duplicates(subset=['UPC'],keep='first') 
    concatenated_rows_save_product_list = concatenated_by_rows.drop_duplicates(subset=['UPC'],keep='last')
    concatenated_rows_save_thumbnail.to_csv(os.path.join(OUTPUT_PATH,'concatenated_rows_save_thumbnail.csv'), sep="\t")
    concatenated_rows_save_product_list.to_csv(os.path.join(OUTPUT_PATH,'concatenated_rows_save_product_list.csv'), sep="\t")

    ######################################################################################################################################################################

    concatenated_by_cols= pd.concat([ upc_thumbnails_df_unique_df, upc_product_list_df_unique_df], axis = 1)
    concatenated_by_cols.columns = ['UPC_thumbnails' , 'UPC_product_list']

    merged_inner = pd.merge(upc_thumbnails_df_unique_df, upc_product_list_df_unique_df, on='UPC', how='inner')
    merged_left = pd.merge(upc_thumbnails_df_unique_df, upc_product_list_df_unique_df, on='UPC', how='left')
    merged_right = pd.merge(upc_thumbnails_df_unique_df, upc_product_list_df_unique_df, on='UPC', how='right')

    concatenated_by_cols.to_csv(os.path.join(OUTPUT_PATH,'thumbnails_product_list_upc_concatenated.csv'), sep="\t")
    merged_inner.to_csv(os.path.join(OUTPUT_PATH,'thumbnails_product_list_upc_inner.csv'), sep="\t")
    merged_left.to_csv(os.path.join(OUTPUT_PATH,'thumbnails_product_list_upc_right.csv'), sep="\t")
    merged_right.to_csv(os.path.join(OUTPUT_PATH,'thumbnails_product_list_upc_left.csv'), sep="\t")
    
    ######################################################################################################################################################################
    return intersection_of_thumnbails_and_product_list,concatenated_by_cols , concatenated_by_rows



def process_data_PL_and_Thumbnails(PRODUCT_LIST_PATH,thumbnailes_upc_list : list ,OUTPUT_PATH : str):

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

    process_data_PL_and_Thumbnails(PRODUCT_LIST_PATH,thumbnailes_upc_list,OUTPUT_PATH) 

    # intersection_of_thumnbails_and_product_list, concatenated_cols_thumbnail_and_product_list,concatenated_rows_thumbnail_and_product_list = fetch_thumbnails_and_product_list_data(NEW_THUMBNAILS_DIR_PATH,thumbnailes_upc_list,OUTPUT_PATH,PRODUCT_LIST_PATH)

    # calc_intersection_upc_thumbnails_product_list(concatenated_rows_thumbnail_and_product_list)

    # pandas_exp_dataset(show = True)

    
if __name__ == "__main__":
    
    main()
