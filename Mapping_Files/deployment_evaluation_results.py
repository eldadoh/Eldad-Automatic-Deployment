import pandas as pd 
import os,glob,shutil

def create_dir_with_override(dir_path):
    try : 
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)
    except Exception as e : 
        print(e)
        print('Could not create the desired dir with the corersponding dir path : \n' + f'{dir_path}')

def load_df_from_csv(csv_file_path:str, sep:str = ',') -> pd.DataFrame :

    df = pd.read_csv(csv_file_path,sep)
    
    return df 


def download_and_log(evaluation_file_paths,RESULTS_DIR_PATH):

    for file_path in evaluation_file_paths :
        
        model_name = os.path.split(file_path)[0]
        model_name = os.path.split(model_name)[-1]
        os.system(f'gsutil -m cp {file_path} {RESULTS_DIR_PATH}')
        src_path = os.path.join(RESULTS_DIR_PATH,'evaluation.csv')
        dist_path = os.path.join(RESULTS_DIR_PATH,f'{model_name}'+'.csv')

        log_file_path = os.path.join(RESULTS_DIR_PATH,'logger.txt')
        with open(f'{log_file_path}', 'a') as f: 
            try: 
                os.rename(src_path,dist_path)
            except Exception as e : 
                f.write(f'\n{e}\n')



def main(): 

    DEPLOYMENT_CSV_PATH = 'Mapping_Files/Data/Deployments_Data_sheets/Dor Alon - CV Models Category Map 14 - DorAlonStores1.csv'
    
    OUTPUT_DIR_PATH ='Mapping_Files/Output/Deployment_Evaluation_Plots'
    RESULTS_DIR_NAME = os.path.split(DEPLOYMENT_CSV_PATH)[-1][:-len('.csv')]
    RESULTS_DIR_NAME = RESULTS_DIR_NAME.replace(' ','_')
    RESULTS_DIR_PATH = os.path.join(OUTPUT_DIR_PATH,RESULTS_DIR_NAME)
    create_dir_with_override(RESULTS_DIR_PATH)

    df = load_df_from_csv(csv_file_path=DEPLOYMENT_CSV_PATH)
    categories_models_list = [item for item in list(df['Category-Model'].unique())]
    specific_models_list = [item for item in list(df['Specific-Model'].unique())]
    models_list = categories_models_list + specific_models_list
    
    dates_data = [item.split(sep='_')[-1] for item in models_list]

    evaluation_file_paths = [os.path.join('gs://shelfauditdec19.appspot.com/CVModels' , date) for date in dates_data]
    evaluation_file_paths = [os.path.join(path , f'{model_name}' + '_results') for path,model_name in zip(evaluation_file_paths,models_list)]
    evaluation_file_paths = [os.path.join(path , 'evaluation.csv') for path in evaluation_file_paths]  
    
    # download_and_log(evaluation_file_paths,RESULTS_DIR_PATH)
    
    

if __name__ == "__main__":
    
    main()

