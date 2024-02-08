import numpy as np
import csv

# 텍스트 파일의 경로
txt_file_path = '/home/nishidalab07/github/6dimension/simulation2/sg/goal_visual.txt'

# CSV 파일의 경로
csv_file_path = '/home/nishidalab07/github/6dimension/simulation2/sg/goal_T.csv'

# 텍스트 파일에서 데이터 읽기
with open(txt_file_path, 'r') as txt_file:
    data = [eval(line) for line in txt_file]

# 데이터를 NumPy 배열로 변환
data_array = np.array(data)

# CSV 파일로 데이터 쓰기
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(data_array)
