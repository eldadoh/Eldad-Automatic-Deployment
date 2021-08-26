import pandas as pd 
import os,glob,shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

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


def download_and_log(evaluation_file_paths,RESULTS_DIR_PATH,LOGS_DIR_PATH):

    for file_path in evaluation_file_paths :
        
        model_name = os.path.split(file_path)[0]
        model_name = os.path.split(model_name)[-1]
        os.system(f'gsutil -m cp {file_path} {RESULTS_DIR_PATH}')
        src_path = os.path.join(RESULTS_DIR_PATH,'evaluation.csv')
        dist_path = os.path.join(RESULTS_DIR_PATH,f'{model_name}'+'.csv')

        log_file_path = os.path.join(LOGS_DIR_PATH,'logger.txt')
        with open(f'{log_file_path}', 'a') as f: 
            try: 
                os.rename(src_path,dist_path)
            except Exception as e : 
                f.write(f'\n{e}\n')

def create_dirs(RESULTS_DIR_PATH,PLOTS_DIR_PATH,LOGS_DIR_PATH):
    create_dir_with_override(RESULTS_DIR_PATH)
    create_dir_with_override(PLOTS_DIR_PATH)
    create_dir_with_override(LOGS_DIR_PATH)

def Plot_evaluations_for_one_model(model_evaluation_file_csv_path,OUTPUT_PATH):

    model_name = os.path.basename(model_evaluation_file_csv_path)[:-len('.csv')]
    df_bbox = load_df_from_csv(csv_file_path=model_evaluation_file_csv_path)
    df_evaluation =load_df_from_csv(csv_file_path=model_evaluation_file_csv_path)

    df_bbox = df_bbox[['Product','Overall_Bbox']]
    df_bbox['Product'] = df_bbox['Product'].str[:30]
    df_evaluation = df_evaluation[['Product','Recall','Precision','Harmonic_Mean']]
    df_evaluation['Product'] = df_evaluation['Product'].str[:30]

    plt.figure()
    df_bbox.plot.bar(x='Product', y='Overall_Bbox', rot=0)
    plt.xticks(rotation=90) 
    plt.savefig(OUTPUT_PATH + f'/{model_name}_bbox')
    df_evaluation.plot.bar(x='Product', y=['Recall','Precision','Harmonic_Mean'], rot=0)
    plt.xticks(rotation=90)
    plt.savefig(OUTPUT_PATH + f'/{model_name}_evaluation.png')
    

    return None 

def Plot_evaluations_for_all_models(RESULTS_DIR_PATH,PLOTS_DIR_PATH):

    [Plot_evaluations_for_one_model(file,PLOTS_DIR_PATH) for file in glob.glob(RESULTS_DIR_PATH + '/*.csv')]
    

def main(): 

    """
    Enter the deployment.csv sheet to 'Data/Deployments_Data_sheets/'
    if you want to override the older plots Turn OVERRIDE = True
    """

    OVERRIDE = False
    DEPLOYMENT_CSV_PATH = 'Data/Deployments_Data_sheets/Dor Alon - CV Models Category Map 15 - DorAlonStores1.csv'
    
    OUTPUT_DIR_PATH ='Output/Deployment_Evaluation_Plots'
    RESULTS_DIR_NAME = os.path.split(DEPLOYMENT_CSV_PATH)[-1][:-len('.csv')]
    RESULTS_DIR_NAME = RESULTS_DIR_NAME.replace(' ','_')
    RESULTS_DIR_PATH = os.path.join(OUTPUT_DIR_PATH,RESULTS_DIR_NAME)
    PLOTS_DIR_PATH = os.path.join(RESULTS_DIR_PATH,'Plots')
    LOGS_DIR_PATH = os.path.join(RESULTS_DIR_PATH,'Logs')
    if OVERRIDE :
        create_dirs(RESULTS_DIR_PATH,PLOTS_DIR_PATH,LOGS_DIR_PATH)

    df = load_df_from_csv(csv_file_path=DEPLOYMENT_CSV_PATH)
    categories_models_list = [item for item in list(df['Category-Model'].unique())]
    specific_models_list = [item for item in list(df['Specific-Model'].unique())]
    models_list = categories_models_list + specific_models_list
    
    # add support for categories split later 

    # df_groups = df.groupby('Category-Model')
    # categories_list = df_groups.size().index.to_list()    
    # categories_models = [df_groups.get_group(f'{category}') for category in categories_list]
    # categories_models = [category_model.to_dict() for category_model in categories_models]
    # # dates_data = [model for model in categories_models for item in model]

    dates_data = [item.split(sep='_')[-1] for item in models_list]
    evaluation_file_paths = [os.path.join('gs://shelfauditdec19.appspot.com/CVModels' , date) for date in dates_data]
    evaluation_file_paths = [os.path.join(path , f'{model_name}' + '_results') for path,model_name in zip(evaluation_file_paths,models_list)]
    evaluation_file_paths = [os.path.join(path , 'evaluation.csv') for path in evaluation_file_paths]  
    
    if OVERRIDE :
        download_and_log(evaluation_file_paths,RESULTS_DIR_PATH,LOGS_DIR_PATH)
    Plot_evaluations_for_all_models(RESULTS_DIR_PATH,PLOTS_DIR_PATH)

if __name__ == "__main__":
    
    main()

