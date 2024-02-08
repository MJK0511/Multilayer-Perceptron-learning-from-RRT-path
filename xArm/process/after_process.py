import os
from ex_and_con_cartesian_all import CtoT
from distance import Distance
from devide import Devide
from csvtotxt import csvtotxt


def after(default_folder):
    # # after_MLP.csv 를 하나의 txt파일로
    CSVtoTXT = csvtotxt()
    input_file_path = os.path.join(default_folder, 'csv/before/testinput.csv')
    output_file_path = os.path.join(default_folder, 'Configuration/After_train/sg.txt')
    CSVtoTXT.csv_to_txt(input_file_path, output_file_path)

    input_file_path = os.path.join(default_folder, 'csv/after/test_ma.csv')
    output_file_path = os.path.join(default_folder, 'Configuration/After_train/ma.txt')
    CSVtoTXT.csv_to_txt(input_file_path, output_file_path)

    input_file_path = os.path.join(default_folder, 'csv/after/test_mb.csv')
    output_file_path = os.path.join(default_folder, 'Configuration/After_train/mb.txt')
    CSVtoTXT.csv_to_txt(input_file_path, output_file_path)

    input_file_path = os.path.join(default_folder, 'csv/after/test_mc.csv')
    output_file_path = os.path.join(default_folder, 'Configuration/After_train/mc.txt')
    CSVtoTXT.csv_to_txt(input_file_path, output_file_path)

    input_file_path = os.path.join(default_folder, 'csv/after/result_all.csv')
    output_file_path = os.path.join(default_folder, 'Configuration/After_train/all.txt')
    CSVtoTXT.csv_to_txt(input_file_path, output_file_path)

    # MLP path(C공간)를 개별 txt로
    devider = Devide()
    input_file_path = os.path.join(default_folder, 'Configuration/After_train/all.txt')
    output_file_path = os.path.join(default_folder, 'Configuration/After_train/allpath')
    devider.devide(input_file_path, output_file_path, 5)

    input_file_path = os.path.join(default_folder, 'Configuration/After_train/sg.txt')
    output_file_path = os.path.join(default_folder, 'Configuration/After_train/sgpath')
    devider.devide(input_file_path, output_file_path, 2)

    # # C공간의 좌표를 T공간의 좌표로 변환 #MLP
    configtotask = CtoT()
    # input_folder_path = os.path.join(default_folder, 'Configuration/After_train')
    # output_folder_path = os.path.join(default_folder, 'Task/After_train')
    # configtotask.process_files(input_folder_path, output_folder_path)

    input_folder_path = os.path.join(default_folder, 'Configuration/After_train/allpath')
    output_folder_path = os.path.join(default_folder, 'Task/After_train/allpath')
    configtotask.process_files(input_folder_path, output_folder_path)

    # 거리 측정 #MLP
    distance = Distance()
    input_folder_path = os.path.join(default_folder, 'Task/After_train/allpath')
    output_folder_path = os.path.join(default_folder, 'distance_MLP.csv')
    distance.save_to_csv(input_folder_path, output_folder_path)

default_folder = '/home/nishidalab07/github/6dimension/simulation2'

after(default_folder)
