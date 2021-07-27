import os
import re
import glob
import shutil 
import pandas as pd 
from src.pandas_utils import load_df_from_csv, save_df_as_csv
import itertools

def main(): 

  fixed_annotations_perfect  = dict()
  fixed_annotations_sku  = dict()

  def perfect_match(x):
      if x in valid_annotations_as_list : 
          fixed_annotations_perfect[f'{x}'] = x 
      return 1 if x in valid_annotations_as_list else 0 

  def sku_match(x):
      if x.split('_')[0] in valid_sku_list :
        try:   
            first_part,second_part = x.split('_')
            new_annotation = first_part + ' - ' + second_part
            if new_annotation in valid_annotations_as_list:
                fixed_annotations_sku[f'{x}'] = new_annotation 
        except: 
            pass
      if x.split(' - ')[0] in valid_sku_list :
       try: 
            first_part,second_part = x.split(' - ')
            new_annotation = first_part + '_' + second_part
            if new_annotation in valid_annotations_as_list:
                fixed_annotations_sku[f'{x}'] = new_annotation 
       except: 
            pass
      return 1 if x.split('_')[0] in valid_sku_list or x.split(' - ')[0] in valid_sku_list else 0 

  def description_match(x):
    #   if x.split('_')[-1] in valid_description_list or x.split(' - ')[-1] in valid_description_list:
    #     fixed_annotations[f'{x}'] = x   
      return 1 if x.split('_')[-1] in valid_description_list or x.split(' - ')[-1] in valid_description_list else 0 
  def description_match_case_senstive(x):
        return 1 if (x.split('_')[-1]).lower() in valid_description_list_case_senstive or (x.split(' - ')[-1]).lower() in valid_description_list_case_senstive else 0 

  VALID_ANNOTATIONS_FILE_PATH = 'Data/Annotation_Verifcation/valid_kids_annotations.csv'
  ANNOTATIONS_TO_CHECK_PATH = 'Data/Annotation_Verifcation/raw/annotations_to_check_3.csv'
  OUTPUT_PATH = 'Outputs/Annotations-Verification'
  
  valid_df = pd.read_csv(VALID_ANNOTATIONS_FILE_PATH,sep=',')
  check_df = pd.read_csv(ANNOTATIONS_TO_CHECK_PATH,sep=',')
   
  valid_annotations_as_list = [list(item).pop() for item in (valid_df.values)]
  valid_sku_list = [[item.split(sep='_')[0] for item in valid_annotations_as_list],[item.split(sep=' - ')[0] for item in valid_annotations_as_list]]
  valid_sku_list = list(itertools.chain(*valid_sku_list))
  valid_description_list = [[item.split(sep='_')[-1] for item in valid_annotations_as_list],[item.split(sep=' - ')[-1] for item in valid_annotations_as_list]]
  valid_description_list = list(itertools.chain(*valid_description_list))
  valid_description_list_case_senstive = [[(item.split(sep='_')[-1]).lower() for item in valid_annotations_as_list],[(item.split(sep=' - ')[-1]).lower() for item in valid_annotations_as_list]]
  valid_description_list_case_senstive = list(itertools.chain(*valid_description_list_case_senstive))
  
  res_df = pd.DataFrame(columns = ['string_to_check'])
  res_df['string_to_check'] = check_df['SKU']
  
  res_df['Perfect_match'] = res_df['string_to_check'].apply(perfect_match)
  res_df['SKU_match'] = res_df['string_to_check'].apply(sku_match)
  res_df['Description_match'] = res_df['string_to_check'].apply(description_match)
  res_df['Description_match_case_senstive'] = res_df['string_to_check'].apply(description_match_case_senstive)
  res_df['_bbox_count'] = check_df['bbox count']
  
  res_df = res_df.sort_values('Perfect_match',ascending=False)
  res_df.to_csv(os.path.join(f'{OUTPUT_PATH}','res_df_kids.csv'),sep='\t')
  
  fixed_annotations_perfect  = pd.DataFrame.from_dict(fixed_annotations_perfect,orient="index").reset_index()
  fixed_annotations_sku  = pd.DataFrame.from_dict(fixed_annotations_sku,orient="index").reset_index()
  res_df.to_csv(os.path.join(f'{OUTPUT_PATH}','fixed_annotations_perfect.csv'),sep='\t')
  res_df.to_csv(os.path.join(f'{OUTPUT_PATH}','fixed_annotations_sku.csv'),sep='\t')

  print()


  

if __name__ == "__main__":

    main()
