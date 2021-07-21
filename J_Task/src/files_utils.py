import os
import csv, json
import glob 
import shutil 

def merge_dicts(d1,d2) : 

    return dict(**d1 , **d2)

def untar_combined_zip_files_to_one(path):
    os.system("mkdir combined")
    os.system("unzip '*.zip' -d combined")

def read_from_txt_file(txt_file_name_path = 'filename'):

    with open(f'{txt_file_name_path}' + '.txt', 'r',encoding="utf8") as f:
        
        all_lines = f.read() #read till the end of the file 
        print(all_lines)

        line = f.readline() #read the next line in the file iterable  
        print(line)

def write_list_to_txt(l,txt_path) : 
    with open(f'{txt_path}.txt', 'w') as f:
        for item in l:
            f.write(f'{item}\n')

def write_list_to_csv(l,csv_path) : 
    with open(csv_path, 'w', newline='\n') as f:
         wr = csv.writer(f, quoting=csv.QUOTE_ALL)
         wr.writerow(l)

def create_dir_with_override(dir_path):
    try : 
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)
    except Exception as e : 
        print(e)
        print('Could not create the desired dir with the corersponding dir path : \n' + f'{dir_path}')

def load_dict_from_csv(csv_file):
    
    reader = csv.reader(open(csv_file, 'r'))
    
    d = {}

    for row in reader:
        
        row = row[0]
        k, v = row.split(sep = '\t')
        d[k] = v
    
    return d 


def main(): 
    
    pass 

if __name__ == "__main__":

    main()