import os
import glob
import csv
from typing import List
from numpy import concatenate
import pandas as pd 
import shutil 

from src.pandas_utils import save_dict_as_df 

def merge_dicts(d1,d2) : 

    try :
         dict(**d1 , **d2)
    except Exception as e: 
        print(f'{e} --> Failure: cant merge dicts')
        print('Probably because there is a common key in both dicts')

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


def fetch_thumbnails_product_list_data(NEW_THUMBNAILS_DIR_PATH : str,thumbnailes_upc_list : list ,OUTPUT_PATH : str , PRODUCT_LIST_PATH : str ) -> csv : 

    upc_thumbnails_df = pd.DataFrame(thumbnailes_upc_list,columns=["UPC"])
    upc_thumbnails_df_unique = upc_thumbnails_df['UPC'].unique() # 611 
    upc_thumbnails_set = set(upc_thumbnails_df_unique)

    product_list_df = load_df_from_csv(PRODUCT_LIST_PATH,sep =',')
    upc_product_list_df = product_list_df['UPC']
    upc_product_list_df_unique = product_list_df['UPC'].unique()
    upc_product_list_set = set(upc_product_list_df_unique) #677 , 668 unique() , 9 duplicates
    upc_product_list_set = {str(num) for num in upc_product_list_df_unique} 

    intersection_of_thumnbails_and_product_list = set.intersection(upc_thumbnails_set, upc_product_list_set)

    
    concatenated_ = pd.concat([upc_thumbnails_df,upc_product_list_df], axis = 1)
    concatenated_.columns = ['UPC_thumbnails' , 'UPC_product_list']

    concatenated_.to_csv(os.path.join(OUTPUT_PATH,'thumbnails_product_list_upc.csv'), sep="\t")
    
    return intersection_of_thumnbails_and_product_list,concatenated_


def fetch_images_from_single_dir_data(IMAGE_DIR_PATH : str,product_name_and_count_dict):

    for sub_dir in os.listdir(IMAGE_DIR_PATH):

        sub_dir_path = os.path.join(IMAGE_DIR_PATH,sub_dir)

        num_of_images = len(glob.glob(sub_dir_path + '/*.jpg'))

        _ , sub_dir_fixed_name = sub_dir.split(sep = '_')

        if sub_dir_fixed_name not in product_name_and_count_dict.keys():
        
            product_name_and_count_dict[sub_dir_fixed_name] = num_of_images
        
        else : 

            print('FAILURE : we  Need to override a key , adding \'DUPLICATE\'')
            print(f'to {sub_dir_fixed_name}')
            product_name_and_count_dict[sub_dir_fixed_name + '_DUPLICATE'] = num_of_images
    
    return product_name_and_count_dict

def fetch_data_from_all_images_dirs(IMAGES_DIR_PATH,OUTPUT_PATH):

    product_name_and_count_dict = dict()

    for sub_dir in os.listdir(IMAGES_DIR_PATH):

        sub_dir_path = os.path.join(IMAGES_DIR_PATH,sub_dir)

        product_name_and_count_dict = fetch_images_from_single_dir_data(sub_dir_path,product_name_and_count_dict)
    
    images_dirs_df = save_dict_as_df(product_name_and_count_dict)

    images_dirs_df = images_dirs_df.sort_index()

    data_file_output_path = os.path.join(OUTPUT_PATH,'images_dirs_data.csv')

    images_dirs_df.to_csv(data_file_output_path)
   
    return data_file_output_path

def main(): 

    IMAGES_DIR_PATH = 'Data/Images_dirs/combined'
    PRODUCT_LIST_PATH = 'Data/Full_Product_List.csv'
    OUTPUT_PATH = 'Outputs' 

    images_dir_data_file_output_path = fetch_data_from_all_images_dirs(IMAGES_DIR_PATH,OUTPUT_PATH)


if __name__ == "__main__":
    
    main()
