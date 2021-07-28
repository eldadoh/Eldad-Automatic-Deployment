import os
import glob
import csv
from typing import List
from numpy import concatenate
import pandas as pd 
import shutil 

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


def process_data(dict_ : dict )-> pd.DataFrame: 
    
    main_data_list,number_of_images_list , path_list = [], [], []
    
    for key in dict_.keys():
        number_of_images ,path = dict_[key]
        number_of_images_list.append(number_of_images)
        path_list.append(path)

    main_data_list = [number_of_images_list,path_list]

    df = pd.DataFrame(main_data_list).T
    df.columns = ['Number_of_images','PATH']


    upc_as_df = pd.DataFrame(dict_.keys())

    images_dirs_df = pd.concat([upc_as_df,df],axis=1)

    images_dirs_df.columns = ['UPC','Number_of_images','PATH']

    images_dirs_df['FROM'] = 'IMAGES_DIRS'
 
    images_dirs_df = images_dirs_df[['UPC','Number_of_images','FROM', 'PATH']] #change order of columns

    images_dirs_df = images_dirs_df.sort_values('UPC')
    
    images_dirs_df = images_dirs_df.reset_index()

    images_dirs_df = images_dirs_df.drop(columns=['index','PATH'])

    return images_dirs_df 

def fetch_data_from_single_images_dir(IMAGE_DIR_PATH : str,product_name_and_count_dict):

    for sub_dir in os.listdir(IMAGE_DIR_PATH):

        sub_dir_path = os.path.join(IMAGE_DIR_PATH,sub_dir)

        num_of_images = len(glob.glob(sub_dir_path + '/*.jpg'))

        _ , sub_dir_fixed_name = sub_dir.split(sep = '_')

        path_to_class = os.path.join(os.path.basename(IMAGE_DIR_PATH),sub_dir)

        if sub_dir_fixed_name not in product_name_and_count_dict.keys():
        
            product_name_and_count_dict[sub_dir_fixed_name] = [num_of_images,path_to_class]
        
        else : 

            print('FAILURE : we  Need to override a key , adding \'DUPLICATE\'')
            print(f'to {sub_dir_fixed_name}')
            product_name_and_count_dict[sub_dir_fixed_name + '_DUPLICATE'] = [num_of_images,path_to_class]

    
    return product_name_and_count_dict

def fetch_data_from_all_images_dirs(IMAGES_DIR_PATH,OUTPUT_PATH):

    product_name_and_count_dict = dict()

    for sub_dir in os.listdir(IMAGES_DIR_PATH):

        sub_dir_path = os.path.join(IMAGES_DIR_PATH,sub_dir)

        product_name_and_count_dict = fetch_data_from_single_images_dir(sub_dir_path,product_name_and_count_dict)

    images_dirs_df = process_data(product_name_and_count_dict)

    data_file_output_path = os.path.join(OUTPUT_PATH,'Raw_df/images_dirs_df.csv')

    images_dirs_df.to_csv(data_file_output_path,sep ='\t')
   
    return data_file_output_path,images_dirs_df

def get_duplicates_from_df (df) : 
    
    df = df[df.duplicated(['UPC'],keep=False)]
    df.to_csv('Outputs/Final/duplicates_in_'+f'{df}' +'.csv')

def main(): 

    IMAGES_DIR_PATH = 'Data/Images_dirs/combined'
    PRODUCT_LIST_PATH = 'Data/Full_Product_List.csv'
    OUTPUT_PATH = 'Outputs' 

    # images_dir_data_file_output_path,images_dirs_df = fetch_data_from_all_images_dirs(IMAGES_DIR_PATH,OUTPUT_PATH)

    data = pd.read_csv('Data/Images_dirs/missing_folders.txt', sep=" ", header=None)
    data.columns = ["UPC"]
    data_file_output_path = os.path.join(OUTPUT_PATH,'Raw_df/images_dirs_df.csv')
    data.to_csv(data_file_output_path,sep ='\t')


if __name__ == "__main__":
    
    main()
