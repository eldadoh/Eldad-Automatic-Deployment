import os
import re
import glob
import shutil 
import pandas as pd 
from src.pandas_utils import load_df_from_csv, save_df_as_csv

def main(): 

  def perfect_match(x):
        return 1 if x in valid_annotations_as_list else 0 

  def sku_match(x):
        return 1 if x.split('_')[0] in valid_sku_list else 0 

  def description_match(x):
        return 1 if x.split('_')[-1] in valid_description_list else 0 
  def description_match_case_senstive(x):
        return 1 if (x.split('_')[-1]).lower() in valid_description_list_case_senstive else 0 

  VALID_ANNOTATIONS_FILE_PATH = 'Data/Annotation_Verifcation/valid_annotations.csv'
  ANNOTATIONS_TO_CHECK_PATH = 'Data/Annotation_Verifcation/raw/annotations_to_check_3.csv'
  OUTPUT_PATH = 'Outputs/Annotations-Verification'
  
  valid_df = load_df_from_csv(VALID_ANNOTATIONS_FILE_PATH)
#   check_df = load_df_from_csv(ANNOTATIONS_TO_CHECK_PATH)
  check_df = pd.read_csv(ANNOTATIONS_TO_CHECK_PATH,sep=',')
   
  valid_annotations_as_list = [list(item).pop() for item in (valid_df.values)]
  valid_sku_list = [item.split(sep='_')[0] for item in valid_annotations_as_list]
  valid_description_list = [item.split(sep='_')[-1] for item in valid_annotations_as_list]
  valid_description_list_case_senstive = [(item.split(sep='_')[-1]).lower() for item in valid_annotations_as_list]
 
  res_df = pd.DataFrame(columns = ['string_to_check'])
  res_df['string_to_check'] = check_df['SKU']
  res_df['Perfect_match'] = res_df['string_to_check'].apply(perfect_match)
  res_df['SKU_match'] = res_df['string_to_check'].apply(sku_match)
  res_df['Description_match'] = res_df['string_to_check'].apply(description_match)
  res_df['Description_match_case_senstive'] = res_df['string_to_check'].apply(description_match_case_senstive)
  
  res_df.to_csv(os.path.join(f'{OUTPUT_PATH}','res_df_3.csv'),sep='\t')

if __name__ == "__main__":

    main()
