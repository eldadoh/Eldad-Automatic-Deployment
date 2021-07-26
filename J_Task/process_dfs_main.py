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
    try: 
        df = df.drop(columns=['Unnamed: 0'])
    except:
        pass
    
    df = df.sort_values(f'{key}')
    df.to_csv(f'{Output_path}/duplicates_in_'+f'{NAME_OF_DF}' +'.csv')


def main(): 

    IMAGES_DIRS__CSV_PATH = 'Outputs/Raw_df/images_dirs_df.csv'
    PRODUCT_LIST__CSV_PATH = 'Outputs/Raw_df/Product_list_df.csv'
    THUMNBAILS_DIR_CSV_PATH = 'Outputs/Raw_df/Thumbnails_df.csv' 

    DUPLICATES_DIR_OUTPUT_PATH = 'Outputs/duplicates_df'
    FINAL_OUTPUTS_DIR_PATH = 'Outputs/Final'

    product_list_df = load_df_from_csv(PRODUCT_LIST__CSV_PATH,sep ='\t')
    images_dir_df = load_df_from_csv(IMAGES_DIRS__CSV_PATH,sep =',')
    thumbnails_df = load_df_from_csv(THUMNBAILS_DIR_CSV_PATH,sep ='\t')

    product_list_df['UPC'] = product_list_df['UPC'].astype(str)
    product_list_df = product_list_df.drop(columns=['Unnamed: 0'])
    product_list_df['Product_List'] = 'Yes' 
    product_list_df.to_csv('Outputs/product_list_df.csv')
    
    images_dir_df['UPC'] = images_dir_df['UPC'].astype(str)
    images_dir_df['Number_of_images'] = images_dir_df['Number_of_images'].astype(str)
    images_dir_df = images_dir_df.drop(columns=['Unnamed: 0','FROM'])
    images_dir_df['Image_Dirs'] = 'Yes' 
    images_dir_df = images_dir_df[['UPC','Image_Dirs','Number_of_images']]
    images_dir_df.to_csv('Outputs/images_dir_df.csv')


    thumbnails_df['UPC'] = thumbnails_df['UPC'].astype(str)
    thumbnails_df = thumbnails_df.drop(columns=['Unnamed: 0'])
    thumbnails_df['Thumbnails'] = 'Yes'
    thumbnails_df.to_csv('Outputs/thumbnails_df.csv')


    product_list_df.shape , images_dir_df.shape ,thumbnails_df.shape #((677, 4), (285, 3)) ,(611, 2)
    product_list_df.dtypes , images_dir_df.dtypes, thumbnails_df.dtypes  # all object dtype

    merged_outer = pd.merge(product_list_df,images_dir_df,how = 'outer' , on = 'UPC') # (682,6)
    merged_inner = pd.merge(product_list_df,images_dir_df,how = 'inner' , on = 'UPC') # (293,6)
    merged_left = pd.merge(product_list_df,images_dir_df,how = 'left' , on = 'UPC') # (677,6)
    merged_right = pd.merge(product_list_df,images_dir_df,how = 'right' , on = 'UPC') # (298,6)

    merged_inner.shape,merged_outer.shape,merged_left.shape,merged_right.shape # ((293, 6), (682, 6), (677, 6), (298, 6))

    res_df = pd.merge(merged_outer,thumbnails_df,how = 'outer' , on = 'UPC') # (293,6)
    res_df[['Product_List','Image_Dirs','Thumbnails']] = res_df[['Product_List','Image_Dirs','Thumbnails']].fillna(value = 'No')
    res_df[['CATEGORY','SUB_CATEGORY','Number_of_images']] = res_df[['CATEGORY','SUB_CATEGORY','Number_of_images']].fillna(value = '--')

    res_df = res_df[['UPC',	'CATEGORY',	'SUB_CATEGORY',	'Product_List',	'Image_Dirs','Thumbnails','Number_of_images']]
    res_df.to_csv('Outputs/res_df.csv')

    # get_duplicates_from_df(product_list_df,'UPC',DUPLICATES_DIR_OUTPUT_PATH,NAME_OF_DF = 'product_list')
    # get_duplicates_from_df(thumbnails_df,'UPC',DUPLICATES_DIR_OUTPUT_PATH,NAME_OF_DF = 'thumbnails_df')
    # get_duplicates_from_df(images_dir_df,'UPC',DUPLICATES_DIR_OUTPUT_PATH,NAME_OF_DF = 'images_dir_df')

if __name__ == "__main__":
    
    main()
