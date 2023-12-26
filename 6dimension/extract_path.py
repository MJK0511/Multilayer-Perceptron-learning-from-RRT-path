#!/usr/bin/env python3
import os
import re
import pandas as pd

input_df1 = pd.DataFrame()
input_df2 = pd.DataFrame()
input_df3 = pd.DataFrame()
output_df1 = pd.DataFrame()
output_df2 = pd.DataFrame()
output_df3 = pd.DataFrame()

s_df = pd.DataFrame()
g_df = pd.DataFrame()
ma_df = pd.DataFrame()
mb_df = pd.DataFrame()
mc_df = pd.DataFrame()

columns_s = [f's{i+1}' for i in range(6)]
columns_g = [f'g{i+1}' for i in range(6)]
columns_ma = [f'ma{i+1}' for i in range(6)]
columns_mb = [f'mb{i+1}' for i in range(6)]
columns_mc = [f'mc{i+1}' for i in range(6)]

# angle 폴더 내의 모든 파일에 대해 반복
learning_folder = '/home/nishidalab07/catkin_ws/src/ws_moveit/src/data_path/learning'

def middle_index(matches) : 
    if matches % 2 == 0: 
        middle_index = matches // 2 - 1
    else:
        middle_index = matches // 2
    return middle_index

for filename in os.listdir(learning_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(learning_folder, filename)

        with open(file_path, 'r') as file:
            data = file.read()
            
            # positions 값을 추출할 정규 표현식
            pattern = r'positions:\s*(\[.*?\])'
            matches = re.findall(pattern, data)
            
            # positions 값이 3개 이상인 경우만 처리
            if len(matches) >= 3:
                middleA_index = middle_index(len(matches))
                middleB_index = middle_index(middleA_index)
                middleC_index = middle_index(middleA_index)+middleB_index
               
                start = [eval(matches[0].replace(']', ']'))]
                middleA = [eval(matches[middleA_index].replace(']', ']'))]
                middleB = [eval(matches[middleB_index].replace(']', ']'))]
                middleC = [eval(matches[middleC_index].replace(']', ']'))]
                goal = [eval(matches[-1].replace(']', ']'))]

                # 각각의 DataFrame에 추가
                s_df = pd.concat([s_df, pd.DataFrame(data = start, columns = columns_s)])
                g_df = pd.concat([g_df, pd.DataFrame(data = goal, columns = columns_g)])
                ma_df = pd.concat([ma_df, pd.DataFrame(data = middleA, columns = columns_ma)])
                mb_df = pd.concat([mb_df, pd.DataFrame(data = middleB, columns = columns_ma)])
                mc_df = pd.concat([mc_df, pd.DataFrame(data = middleC, columns = columns_ma)])


# Learning Dataset
## start, middleA, goal
input_df1 = pd.concat([input_df1, s_df, g_df], axis=1)
output_df1 = pd.concat([output_df1, ma_df]) 
input_df1.to_csv('input1.csv', index=False)
output_df1.to_csv('output1.csv', index=False)

## start, middleB, middleA
input_df2 = pd.concat([input_df2, s_df, ma_df], axis=1)
output_df2 = pd.concat([output_df2, mb_df]) 
input_df2.to_csv('input2.csv', index=False)
output_df2.to_csv('output2.csv', index=False)

## middleA, middleC, goal
input_df3 = pd.concat([input_df3, ma_df, g_df], axis=1)
output_df3 = pd.concat([output_df3, mc_df]) 
input_df3.to_csv('input3.csv', index=False)
output_df3.to_csv('output3.csv', index=False)



