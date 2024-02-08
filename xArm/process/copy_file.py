import os
import re
import shutil

class Copy:
    def copy_files(self, path_A, path_B, path_C):
        number_list = []

        # path_A에서 파일 목록 가져오기
        file_list_A = os.listdir(path_A)

        for file_name in file_list_A:
            if file_name.endswith(".txt"):
                numbers_in_filename = re.findall(r'\d+', file_name)
                
                # 추출된 숫자가 있다면 number_list에 추가
                if numbers_in_filename:
                    number_list.extend(map(int, numbers_in_filename))

        print("File Numbers in path_A:", number_list)

        for file_number in number_list:
            origin_file_path = os.path.join(path_B, f'path_{file_number}_R_visual.txt')
            destination_file_path = os.path.join(path_C, f'path_{file_number}.txt')

            if os.path.exists(origin_file_path):
                shutil.copy(origin_file_path, destination_file_path)
                print(f'File path_{file_number}_R_visual.txt copied successfully.')
            else:
                print(f'File path_{file_number}_R_visual.txt not found in {path_B}.')

# default_folder = '/home/nishidalab07/github/6dimension/simulation2'

# path_A = os.path.join(default_folder, 'Configuration/selected_op')
# path_B = os.path.join(default_folder, 'Task/extract_angle')
# path_C = os.path.join(default_folder, 'Task/selected_op')

# copy_instance = Copy()
# copy_instance.copy_files(path_A, path_B, path_C)
