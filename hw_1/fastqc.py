import zipfile
import os
import pandas as pd
import sys

dir_name = input('Please enter the zip file absolute folder: ')
whether_to_delete_zip = input('Do you want to delete .zip file?(y/n): ')
#dir_name = "/Users/Kuan-Hao/Documents/大二下/專題研究-莊曜宇/Zip/"
file_extension = ".zip"
os.chdir(dir_name)

file_name_list = pd.Series()
counter_file = 0
ansList = pd.Series()
counter_ans = 0
start_row = 0
end_row = 0

# stackoverflow: https://stackoverflow.com/questions/31346790/unzip-all-zipped-files-in-a-folder-to-that-same-folder-using-python-2-7-5
for item in os.listdir(dir_name):
    if item.endswith(file_extension):
        file_name_abs = os.path.abspath(item)
        file_name_loc = os.path.basename(item)
        file_name_list = file_name_list.set_value(label = counter_file, value = file_name_loc)
        counter_file+=1
        zip_ref = zipfile.ZipFile(file_name_abs) # extract file to dir
        zip_ref.extractall(dir_name) # extracted file and put in to dir_name
        zip_ref.close() # close the extracted file
        if whether_to_delete_zip == 'y' or whether_to_delete_zip == 'Y' or whether_to_delete_zip == 'yes' or whether_to_delete_zip == 'Yes':
            os.remove(file_name_abs) # delete zipped file

# stackoverfolw: https://stackoverflow.com/questions/5817209/browse-files-and-subfolders-in-python
for root, dirs, files in os.walk(dir_name):
    for name in files:
        if name == "fastqc_data.txt":
            data_first = pd.read_csv(filepath_or_buffer = root+'/fastqc_data.txt', error_bad_lines=False, header = None )

            inside_loop = False
            for x in range(0,len(data_first)-1):
                if data_first[0][x] == "#Quality\tCount":
                    start_row = x
                    inside_loop = True
                if(inside_loop == True):
                    if data_first[0][x] == ">>END_MODULE":
                        end_row = x
                        break

            data_second = pd.read_csv(filepath_or_buffer = root+'/fastqc_data.txt', error_bad_lines=False, sep = '\t',header = start_row )
            dataSelect = data_second.loc[0:end_row-start_row-2]
            ansSum_all = 0
            ansSum_above30 = 0
            for x in range(0, len(dataSelect["#Quality"])):
                ansSum_all += float(dataSelect["Count"][x])
                if int(dataSelect["#Quality"][x]) >= 30:
                    ansSum_above30 += float(dataSelect["Count"][x])
            ans = ansSum_above30/ansSum_all
            ansList = ansList.set_value(label = counter_ans, value = ans)
            counter_ans += 1
            
final_ans_csv = pd.concat([file_name_list, ansList], axis = 1)
final_ans_csv.to_csv(dir_name+'/finalAns.csv', encoding='utf-8', index=False) 

print("Finish! The file is in the same folder")
            
            