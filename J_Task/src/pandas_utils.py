import pandas as pd 
import numpy as np

def load_df_from_csv(csv_file_path:str) -> pd.DataFrame :

    df = pd.read_csv(csv_file_path,sep='\t')

    return df 

def load_df_from_pkl(name : str) -> pd.DataFrame :

    if '.pkl' in name : 

        return pd.read_pickle(name)

def load_df_from_xl(file_name,sheet_name = None):
    
    xl_file = pd.ExcelFile(file_name)

    dfs = {sheet_name: xl_file.parse(sheet_name) 
          for sheet_name in xl_file.sheet_names}

    if sheet_name:
          
          return dfs[f'{sheet_name}']

    return dfs 

def load_df_from_dict(dict_): 

    return pd.DataFrame.from_dict([dict_])
    # return pd.DataFrame.from_dict(dict_, orient='index') # if you want keys  be the index names . 

def save_dict_as_df(dict_ : dict )-> pd.DataFrame: 

    return pd.DataFrame.from_dict(dict_,orient='index')

def load_series_from_dict(dict_):
    return pd.Series(dict_)

def save_df_as_csv(df : pd.DataFrame,name:str):

    """float_format='{:5f}'"""
    
    if '.csv' in name :
        df.to_csv(f'{name}', sep = '\t' , float_format='{:5f}'.format, encoding='utf-8')
    else: 
        print('\nError: You didnt entered \'.csv\'')
    
def save_df_as_pkl(df : pd.DataFrame , name : str , verbose = True) -> None :
    
    if '.pkl' in name : 

        df.to_pickle(name)
        
        if verbose : 
            print (f'\nSaved {name}')

def change_col_dtype(df,col_name, new_dtype = 'int32'):

    df[col_name] =  df[col_name].astype(new_dtype)
    return df 

def sort_df_by_one_columns_values(df,col_name): 

    return df.sort_values(f'{col_name}')

def sort_column_df_values_and_dont_change_order_of_other_columns_values(df): 
    """
    df=
        A B
        1 5
        2 6
        3 8
        4 1
    """
    df['B'] = df['B'].sort_values(ascending=False).values # or 
    df['B'] = df['B'].sort_values(ascending=False).tolist()

    """ 
       A  B
    0  1  8
    1  2  6
    2  3  5
    3  4  1
    """



def find_intersection_between_df(df1,df2):
    
    # intersection == same values for all the columns.

    return df1.merge(df2) 

def series_operations() : 

    s = pd.Series([4, 7, -5, 3], index=['d', 'b', 'a', 'c'])
    index_list = s.index
    get_value_by_key = s['a']
    get_values_by_keys_list = s[['c', 'a', 'd']]
    check_if_key_is_in_series = 'e' in s    
    
    #(users[(users.age == 40) & (users.sex == 'M')].head(3))
    #df.columns = ['a', 'b']