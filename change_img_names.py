import os
import glob
import csv
import argparse 

def get_changes_dict(csv_file):
    
    reader = csv.reader(open(csv_file, 'r'))
    
    changes_dict = {}

    for row in reader:
        
        k, v = row[0].split(sep = '\t')
        changes_dict[k] = v
    
    return changes_dict

def change_image_names(image_dir_path,name_csv_file_path):

    changes_dict = get_changes_dict(name_csv_file_path)

    for img_path in glob.glob(f'{image_dir_path}/*.png'):

        name_to_look_for = os.path.basename(img_path)[:-len('.png')]

        if name_to_look_for in changes_dict : 

            img_new_name_path = os.path.join(os.path.dirname(img_path),changes_dict[name_to_look_for] + '.png')
            os.rename(img_path, img_new_name_path)
            img_name = os.path.basename(img_path)
            print(f'changed {img_name} to {changes_dict[name_to_look_for]}.png')
            
def main(): 

    # NAMES_CSV_FILE_PATH = 'change-images-names-script/names_dict.csv'
    # IMAGES_DIR_PATH = 'ThumbnailsUpload'

    # os.chdir('change-images-names-script')

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--name_csv_file_path', type=str,default='names_dict.csv', help='info :key:old name , value : new name to set')
    parser.add_argument('-j', '--image_dir_path', type=str, default='Data/',help='info: path to images_dir')
    
    args = parser.parse_args()

    change_image_names(args.image_dir_path, args.name_csv_file_path)


if __name__ == "__main__":
    
    main()
    #usage: python3 change_img_names.py -i {names_csv_file_path} -o {image_dir_path}