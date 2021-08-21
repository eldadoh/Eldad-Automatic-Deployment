import os
import glob
import csv
import pandas as pd 
import shutil 

def load_df_from_csv(csv_file_path:str, sep:str = ',') -> pd.DataFrame :

    df = pd.read_csv(csv_file_path,sep)
    
    return df 

def get_duplicates_from_df (df,key,Output_path,NAME_OF_DF) : 
    
    df = df[df.duplicated(f'{key}',keep=False)]
    try: 
        df = df.drop(columns=['Unnamed: 0'])
    except Exception as e:
        print(e)
        pass
    
    df = df.sort_values(f'{key}')
    df.to_csv(f'{Output_path}/duplicates_in_'+f'{NAME_OF_DF}' +'.csv')


def main(): 

    DAIRY_OLD_PATH = 'J_Task/Data/Dor-alon-files/sku-old.csv'
    DAIRY_NEW_PATH = 'J_Task/Data/Dor-alon-files/sku-new.csv'


    dairy_old_df = load_df_from_csv(DAIRY_OLD_PATH,sep ='\t')
    dairy_new_df = load_df_from_csv(DAIRY_NEW_PATH,sep ='\t')

    # product_list_df['UPC'] = product_list_df['UPC'].astype(str)
    # product_list_df = product_list_df.drop(columns=['Unnamed: 0'])
    # product_list_df['Product_List'] = 'Yes' 
    # product_list_df.to_csv('Outputs/product_list_df.csv')
    
    # images_dir_df['UPC'] = images_dir_df['UPC'].astype(str)
    # # images_dir_df['Number_of_images'] = images_dir_df['Number_of_images'].astype(str)
    # images_dir_df = images_dir_df.drop(columns=['Unnamed: 0'])
    # images_dir_df['Image_Dirs'] = 'Yes' 
    # # images_dir_df = images_dir_df[['UPC','Image_Dirs','Number_of_images']]
    # # images_dir_df = images_dir_df[['UPC']]
    # images_dir_df.to_csv('Outputs/images_dir_df.csv')


    # thumbnails_df['UPC'] = thumbnails_df['UPC'].astype(str)
    # thumbnails_df = thumbnails_df.drop(columns=['Unnamed: 0'])
    # thumbnails_df['Thumbnails'] = 'Yes'
    # thumbnails_df.to_csv('Outputs/thumbnails_df.csv')


    # product_list_df.shape , images_dir_df.shape ,thumbnails_df.shape #((677, 4), (285, 3)) ,(611, 2)
    # product_list_df.dtypes , images_dir_df.dtypes, thumbnails_df.dtypes  # all object dtype


    merged_outer = pd.merge(dairy_new_df,dairy_old_df,how = 'outer' , on = 'SKU')
    merged_inner = pd.merge(dairy_new_df,dairy_old_df,how = 'inner' , on = 'SKU') # (293,6)
    merged_left =  pd.merge(dairy_new_df,dairy_old_df,how = 'left' , on = 'SKU') # (677,6)
    merged_right = pd.merge(dairy_new_df,dairy_old_df,how = 'right' , on = 'SKU') # (298,6)

    merged_inner.shape,merged_outer.shape,merged_left.shape,merged_right.shape # ((293, 6), (682, 6), (677, 6), (298, 6))

    # res_df = pd.merge(merged_outer,thumbnails_df,how = 'outer' , on = 'UPC') # (293,6)
    # res_df[['Product_List','Image_Dirs','Thumbnails']] = res_df[['Product_List','Image_Dirs','Thumbnails']].fillna(value = 'No')
    # res_df[['CATEGORY','SUB_CATEGORY']] = res_df[['CATEGORY','SUB_CATEGORY']].fillna(value = '--')

    # res_df = res_df[['UPC',	'CATEGORY',	'SUB_CATEGORY',	'Product_List',	'Image_Dirs','Thumbnails']]
    # res_df.to_csv('Outputs/res_df.csv')


if __name__ == "__main__":
    
    main()
