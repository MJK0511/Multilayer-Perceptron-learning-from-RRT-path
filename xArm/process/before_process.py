import os
from extract_angle_all import extract_C_all
from ex_and_con_cartesian_all import CtoT
from extract_path import extract_middle
from check import Check
from distance import Distance
from copy_file import Copy

def before(default_folder):
    # RRT로 path 생성 직후   
    # RRT path로부터 모든 positions를 추출 
    extractor = extract_C_all()
    input_folder_path = os.path.join(default_folder, 'Configuration/originpath/yet')
    output_folder_path = os.path.join(default_folder, 'Configuration/extract_angle')
    extractor.process_files_in_directory(input_folder_path, output_folder_path)

    # C공간의 좌표를 T공간의 좌표로 변환 #RRT
    ctot = CtoT()
    input_folder_path = os.path.join(default_folder, 'Configuration/extract_angle')
    output_folder_path = os.path.join(default_folder, 'Task/extract_angle')
    ctot.process_files(input_folder_path, output_folder_path)

def Configuration(default_folder):
    #Copy C to T
    copipe = Copy()
    path_A = os.path.join(default_folder, 'Configuration/selected_op')
    path_B = os.path.join(default_folder, 'Task/extract_angle')
    path_C = os.path.join(default_folder, 'Task/selected_op')
    copipe.copy_files(path_A, path_B, path_C)

    # # select 완료 이후 
    # # RRT path가 몇 개의 waypoint로 구성되어있는가
    # checker = Check()
    # input_folder_path = os.path.join(default_folder, 'Configuration/selected_op')
    # output_folder_path = os.path.join(default_folder, 'check.csv')
    # checker.process_directory(input_folder_path, output_folder_path)

    # before_MLP path를 추출 (csv)
    # extractM = extract_middle()
    # input_folder_path = os.path.join(default_folder, 'Configuration/selected_op')
    # test_folder_path = os.path.join(default_folder, 'Configuration/test')
    # output_folder_path = os.path.join(default_folder, 'csv/before') 
    # extractM.save_to_csv(input_folder_path, test_folder_path, output_folder_path)

    # 거리 측정 #RRT
    distance = Distance()
    # input_folder_path = os.path.join(default_folder, 'Task/selected_op')
    # output_folder_path = os.path.join(default_folder, 'distance_RRT.csv')
    input_folder_path = os.path.join(default_folder, 'Task/extract_angle/sample')
    output_folder_path = os.path.join(default_folder, 'distance_RRT_sample.csv')
    distance.save_to_csv(input_folder_path, output_folder_path)

default_folder = '/home/nishidalab07/github/6dimension/simulation2'

# before(default_folder)
Configuration(default_folder)