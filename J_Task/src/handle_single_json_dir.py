import json
import csv
import pandas as pd
import numpy as np 
import os
import glob
import shutil 

def convert_top_left_bottom_rigth_to_xywh(top_left,bottom_right,W,H):
    
    top,left = top_left[:]
    bottom,right = bottom_right[:]
    

    w = int(right - left) / W 
    h = int(bottom - top) / H
    x = ((left + right) / 2) / W
    y = ((top + bottom) / 2) / H 

    return x,y,w,h

def handle_single_json_image(json_file,parent_dir,print = False):

    missing_annotations = []

    with open(json_file, 'r') as f:

        data = json.load(f)

        W,H = data['size']['width'],data['size']['height']

        annotations_list = data['objects'][:]

        single_image_annotations_list = []

        for item in annotations_list : 

            img_name =os.path.join(parent_dir ,os.path.basename(json_file)[:-len('.json')])
            
            c = item['classTitle'] 
            
            top_left,bottom_right = item['points']['exterior'][:]

            x,y,w,h = convert_top_left_bottom_rigth_to_xywh(top_left,bottom_right,W,H)

            sample_dict = { 'img_name' : img_name,
                            'class' : c, 
                            'x' : x,
                            'y' : y,
                            'w' : w,
                            'h' : h}
            
            single_annotation_df = pd.DataFrame.from_dict([sample_dict])  

            single_image_annotations_list.append(single_annotation_df)
            
        try :
            single_image_annotations_df = pd.concat(single_image_annotations_list, ignore_index=True)   
            return single_image_annotations_df , []
        except: 
            if print: 
                print(f'\nImage with no annotations: ------- {json_file} ------\n')
            missing_annotations.append(json_file)
            single_image_annotations_df = pd.DataFrame()
            return single_image_annotations_df , missing_annotations
                   

def handle_single_json_product_dir(json_dir_path):

    single_product_annotations_list = []
    
    missing_annotations_for_this_dir = []

    for json_file in glob.glob(json_dir_path +'/*.json'):

        single_image_annotations_df , missing_annotations = handle_single_json_image(json_file,json_dir_path)
        single_product_annotations_list.append(single_image_annotations_df)
        missing_annotations_for_this_dir.append(missing_annotations)

    single_product_annotations_df = pd.concat(single_product_annotations_list, ignore_index=True)    

    return single_product_annotations_df,missing_annotations_for_this_dir


def handle_json_all_products_dir(json_main_path,save = True,print = False):

    all_products_annotations_list = []

    missing_annotations_all_json_dirs = []

    for product_dir in os.listdir(json_main_path):
        
        product_dir_path = os.path.join(json_main_path,product_dir)

        single_product_annotations_df, missing_annotations_for_this_dir = handle_single_json_product_dir(product_dir_path)
        all_products_annotations_list.append(single_product_annotations_df)
        missing_annotations_all_json_dirs.append(missing_annotations_for_this_dir)


    single_product_annotations_df = pd.concat(all_products_annotations_list, ignore_index=True)    

    missing_result_list = []
    if save: 
       for item in missing_annotations_all_json_dirs:   
           for sublist in item : 
               if len(sublist) != 0 : 
                   missing_result_list.append(sublist)
        
       with open('Output/missing_result_list.csv', 'w', newline='\n') as f:
            for item in missing_result_list:
                wr = csv.writer(f, quoting=csv.QUOTE_ALL)
                wr.writerow(item)

       if print : 
                   print('\nThe next images has no annotations at all ! :\n')
                   [print(item) for item in missing_result_list]        

    return single_product_annotations_df , missing_result_list  

if __name__ == '__main__':

    # json_dir_path  = 'Data/annotations/json/0011110353986'
    # handle_single_json_product_dir(json_dir_path)

    JSON_MAIN_DIR_PATH = 'Data/annotations/json'

    handle_json_all_products_dir(JSON_MAIN_DIR_PATH,save = True,print = False)
    