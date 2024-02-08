import os
import pandas as pd
import shutil

class RangeofVal:
    def rangeofval(self, df):
        # simulation1 범위
        # result = df[(0.2 < df['mx']) & (df['mx'] < 0.3) & (-0.4 < df['my']) & (df['my'] < -0.3) & (0.3 < df['mz']) & (df['mz'] < 0.5)] #0101
        # result = df[(0.1 < df['mx']) & (df['mx'] < 0.3) & (-0.4 < df['my']) & (df['my'] < -0.2) & (0.3 < df['mz']) & (df['mz'] < 0.4)] #0102
        # result = df[(0.2 < df['mx']) & (df['mx'] < 0.3) & (-0.4 < df['my']) & (df['my'] < -0.3) & (0.3 < df['mz']) & (df['mz'] < 0.5)] #0201
        # result = df[(0.1 < df['mx']) & (df['mx'] < 0.2) & (-0.4 < df['my']) & (df['my'] < -0.2) & (0.3 < df['mz']) & (df['mz'] < 0.5)] #0202

        # simulation1 : 0001~0202 구분
        # result = df[(0.0 <= df['sz']) & (df['sz'] <= 0.1) & (0.0 <= df['gz']) & (df['gz'] <= 0.1)] #s 00.01 ~ g 00.01 
        # result = df[(0.0 <= df['sz']) & (df['sz'] <= 0.1) & (0.1 <= df['gz']) & (df['gz'] <= 0.2)] #s 00.01 ~ g 01.02 
        # result = df[(0.1 <= df['sz']) & (df['sz'] <= 0.2) & (0.0 <= df['gz']) & (df['gz'] <= 0.1)] #s 01.02 ~ g 00.01 
        # result = df[(0.1 <= df['sz']) & (df['sz'] <= 0.2) & (0.1 <= df['gz']) & (df['gz'] <= 0.2)] #s 01.02 ~ g 01.02 
        
        # simulation2
        # result = df[(0.2 < df['mx']) & (df['mx'] < 0.4) & (0.0 < df['my']) & (df['my'] < 0.2) & (0.85 < df['mz']) & (df['mz'] < 1.1)] # +
        # result = df[(0.3 < df['mx']) & (df['mx'] < 0.5) & (0.0 < df['my']) & (df['my'] < 0.2) & (0.83 < df['mz']) & (df['mz'] < 1.1)] # -
        # result = df[(0.2 < df['mcx']) & (df['mcx'] < 0.3) & (0.2 < df['mcy']) & (df['mcy'] < 0.3) & (0.85 < df['mcz']) & (df['mcz'] < 1.2)] # +
        result = df[(0.0 < df['mcx']) & (df['mcx'] < 0.2) & (0.2 < df['mcy']) & (df['mcy'] < 0.27) & (0.85 < df['mcz']) & (df['mcz'] < 1.2)] #-

        # simulation2
        # gX:0.0을 기준으로 -, +로 나누기 
        # result = df[(0.0 <= df['gx'])] # +
        # result = df[(df['gx'] <= 0.0)] # -

        return result

    def copy_files(self, default_path):
        # Step 1: Read 'filename' column from default/selected.csv
        csv_path = os.path.join(default_path, 'selected.csv')
        df = pd.read_csv(csv_path)
        filenames = df['filename']

        # Step 2: Copy files to default/selected_originpath
        for filename in filenames:
            file_number = ''.join(filter(str.isdigit, filename))
            print(file_number)
            origin_file_path = os.path.join(default_path, f'Configuration/originpath/path_{file_number}.txt')
            destination_file_path = os.path.join(default_path, f'Configuration/selected_op/minus/path_{file_number}.txt')

            # origin_file_path = os.path.join(default_path, f'Task/extract_angle/path_{file_number}_R_visual.txt')
            # destination_file_path = os.path.join(default_path, f'Task/minus/path_{file_number}.txt')
            
            # origin_file_path = os.path.join(default_path, f'Task/extract_angle/path_{file_number}_R_visual.txt')
            # destination_file_path = os.path.join(default_path, f'Task/selected_op/path_{file_number}.txt')

            if os.path.exists(origin_file_path):
                shutil.copy(origin_file_path, destination_file_path)
                print(f'File {filename} copied successfully.')
            else:
                print(f'File {filename} not found in {default_path}Configuration/originpath.')
