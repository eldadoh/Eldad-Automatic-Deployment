from annotations_file_preprocess import handle_all_csv_dirs
from files_utils import create_dir_with_override
import pandas as pd
import numpy as np 
import os
import glob
import shutil 
import json
import csv
from pandas.core.frame import DataFrame
from pandas.io.parsers import read_csv 
from pandas_utils import load_df_from_csv, save_df_as_csv

""" In this file I am running some analysis functions on the clear aggeregated annotations files data"""

def get_specific_class_samples(df_as_csv ,class_name: str,output_dir_path :str , save: bool = False , class_names_who_changed : list = None):

    df = pd.read_csv(df_as_csv,sep='\t')

    specific_class_df = df[df['annotation'] == class_name]

    number_of_samples = specific_class_df.shape[0]
    
    if specific_class_df.empty:
        print(f'Could not get ==={class_name}=== samples from current dataframe because it\'s empty')
    
    if save : 
        output_path = os.path.join(output_dir_path , f'{class_name}.csv')
        try:
            save_df_as_csv(specific_class_df,output_path)
            print(f'\nSaved df samples from class === {class_name} === to : {output_path}\n')
        except:
            print(f'\nBad class name: {class_name}')
            class_name = class_name.replace("/", "@" , -1)
            output_path = os.path.join(output_dir_path , f'{class_name}.csv')
            save_df_as_csv(specific_class_df,output_path)
            print(f'\nChanged and Saved df samples from class === {class_name} === to : {output_path}\n')
            class_names_who_changed.append(class_name)
    
    return specific_class_df,class_names_who_changed , class_name , number_of_samples

def get_all_dataset_specific_class_anotations(df_as_csv : pd.DataFrame,output_path :str , save : bool = False,class_names_who_changed : list = [],verbose :bool = True ):
    """
    1. splits the aggregated big annotations file of all products to sepreate class annotations files
    2. creates annotations_count report  
    """
    df = pd.read_csv(df_as_csv,sep='\t')
    class_names_list = df['annotation'].unique()
    annotations_count_dict = {}

    for class_name in class_names_list : 
        _ , class_names_who_changed,class_name,number_of_samples = get_specific_class_samples(df_as_csv,class_name,output_path,save,class_names_who_changed)
        annotations_count_dict[f'{class_name}'] = number_of_samples
    
    annotations_count_df = pd.DataFrame.from_dict(annotations_count_dict,orient='index',columns= ['number_of_annotations'])
    annotations_count_report_path  = os.path.join(os.path.dirname(output_path),'annotations_count_df.csv')
    save_df_as_csv(annotations_count_df,annotations_count_report_path)

    if verbose: 
        print('The next classes names had changed:\n')
        [print(item) for item in class_names_who_changed]

    return annotations_count_report_path

def creates_annotations_count_less_than_TH_report(csv_file,output_path,Th = 100):

    df = load_df_from_csv(csv_file)
    df = df[df['number_of_annotations'] < Th]
    df.columns = ['class' , 'number_of_annotations']
    output_path = os.path.join(output_path,'annotations_count_less_than_Th.csv')
    save_df_as_csv(df,output_path)

def creates_annotations_suspected_as_w_h_outliers_report(csv_file,output_path,w_th = 0.1 , h_th = 0.1 ):

    df = load_df_from_csv(csv_file)
    df = df[df['width'] < w_th]
    df = df[df['height'] < h_th] 
    output_path = os.path.join(output_path,'annotations_suspected_as_w_h_outliers.csv')
    save_df_as_csv(df,output_path)
        

def main():     

    

    MAIN_ANNOTATIONS_DIR_PATH_CSV = 'Data/annotations/csv'
    MAIN_ANNOTATIONS_DIR_PATH_JSON = 'Data/annotations/json'
    PARAM_DICT ={'annotation_file_name_const' : 'annotations.csv'}
    
    GENERAL_OUTPUT_PATH = 'Output'
    ANNOTATIONS_BY_CLASS_DIR_PATH = 'Output/annotations_by_class'
    MAIN_DF_AS_CSV_FILE_PATH = 'Output/clear_df.csv'
    
    create_dir_with_override(GENERAL_OUTPUT_PATH)
    create_dir_with_override(ANNOTATIONS_BY_CLASS_DIR_PATH)

    handle_all_csv_dirs(MAIN_ANNOTATIONS_DIR_PATH_CSV,param_dict=PARAM_DICT,save=True)
    annotations_count_report_path = get_all_dataset_specific_class_anotations(MAIN_DF_AS_CSV_FILE_PATH,output_path=ANNOTATIONS_BY_CLASS_DIR_PATH,save = True)
    creates_annotations_count_less_than_TH_report(annotations_count_report_path , GENERAL_OUTPUT_PATH , Th = 100 )
    creates_annotations_suspected_as_w_h_outliers_report(MAIN_DF_AS_CSV_FILE_PATH,GENERAL_OUTPUT_PATH,w_th = 0.05 , h_th = 0.05 )

if __name__ == '__main__':
    main()