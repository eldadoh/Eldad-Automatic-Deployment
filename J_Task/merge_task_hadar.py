import pandas as pd 
import os,glob

def load_df_from_csv(csv_file_path:str) -> pd.DataFrame :

    df = pd.read_csv(csv_file_path,sep='\t')
    
    return df 

def load_df_from_xl(file_name,sheet_name = None):
    
    xl_file = pd.ExcelFile(file_name)

    dfs = {sheet_name: xl_file.parse(sheet_name) 
          for sheet_name in xl_file.sheet_names}

    if sheet_name:
          
          return dfs[f'{sheet_name}']

    return dfs 

def tests(test_num,res_df,res_df_1,res_df_2):

    if test_num == 1: 
        res_df_1.merge(res_df_2,on ='SKU', how = 'inner') #sanity check --> should return empty df
    
    if test_num == 2:
        res_df[~res_df.all(axis=1)]
        res_df.iloc[11:12,:]


def main():

    DF_ALL_TIME_PL_PATH = 'Data/merge-task-Hadar/large_PL.xlsx'
    IN_HOUSE_PL_PATH = 'Data/merge-task-Hadar/in-house-PL.tsv'
    df_all_time_PL = load_df_from_xl(DF_ALL_TIME_PL_PATH,sheet_name='Sheet1')
    in_house_PL = load_df_from_csv(IN_HOUSE_PL_PATH)

    #pre-processing

    df_all_time_PL = df_all_time_PL[['SKU-KEY','Y','X','Z']]
    df_all_time_PL.columns = ['SKU','Width','Height','Depth']
    convert_dict = {'SKU': int,'Width': float,'Height': float,'Depth': float}
    df_all_time_PL = df_all_time_PL.astype(convert_dict)
    df_all_time_PL.loc[:,'Width'] = df_all_time_PL.loc[:,'Width'] / 100
    df_all_time_PL.loc[:,'Height'] = df_all_time_PL.loc[:,'Height'] / 100
    df_all_time_PL.loc[:,'Depth'] = df_all_time_PL.loc[:,'Depth'] / 100

    in_house_PL_copy = in_house_PL #use later for the output df 
    in_house_PL = in_house_PL[['SKU','Width','Height','Depth']]

    df_1 = in_house_PL.merge(df_all_time_PL,on ='SKU', how = 'inner') 
    res_df_1 = df_1[['SKU','Width_y','Height_y','Depth_y']]
    res_df_1.columns = ['SKU','Width','Height','Depth']

    df_2 = in_house_PL.merge(df_all_time_PL,on ='SKU', how = 'left') 
    mask = df_2.isna()
    res_df_2 = df_2[mask.any(axis = 1)]

    res_df_2 = res_df_2[['SKU','Width_x','Height_x','Depth_x']]
    res_df_2.columns = ['SKU','Width','Height','Depth']

    res_df = pd.concat([res_df_1, res_df_2])
    res_df = res_df.reset_index()
    res_df = res_df[['SKU','Width','Height','Depth']]
    res_df = res_df.sort_values('SKU')
    res_df = res_df.reset_index(drop=True)

    in_house_PL_copy  = in_house_PL_copy.sort_values('SKU').reset_index(drop = True)
    in_house_PL_copy[['SKU','Width','Height','Depth']] = res_df[['SKU','Width','Height','Depth']]
    in_house_PL_copy  = in_house_PL_copy.sort_values('Class-Name').reset_index(drop = True)
    in_house_PL_copy = in_house_PL_copy.fillna(value = '')
    in_house_PL_copy.to_csv('./Outputs/PL-updated.csv')

if __name__ == "__main__":

    main()


