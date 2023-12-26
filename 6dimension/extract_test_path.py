#!/usr/bin/env python3
import os
import re
import pandas as pd

input_df = pd.DataFrame()
output_df = pd.DataFrame()
test_df = pd.DataFrame()
s_df = pd.DataFrame()
g_df = pd.DataFrame()

columns_s = [f's{i+1}' for i in range(6)]
columns_g = [f'g{i+1}' for i in range(6)]

test_folder = '/home/nishidalab07/catkin_ws/src/ws_moveit/src/data_path/test'

for filename in os.listdir(test_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(test_folder, filename)

        with open(file_path, 'r') as file:
            data = file.read()
            
            # positions 값을 추출할 정규 표현식
            pattern = r'positions:\s*(\[.*?\])'
            matches = re.findall(pattern, data)
            
            # positions 값이 3개 이상인 경우만 처리
            if len(matches) >= 3:
                start = [eval(matches[0].replace(']', ']'))]
                goal = [eval(matches[-1].replace(']', ']'))]

                # 각각의 DataFrame에 추가
                s_df = pd.concat([s_df, pd.DataFrame(data = start, columns = columns_s)])
                g_df = pd.concat([g_df, pd.DataFrame(data = goal, columns = columns_g)])

# Test Dataset
test_df = pd.concat([test_df, s_df, g_df], axis=1)
test_df.to_csv('testinput.csv', index=False)