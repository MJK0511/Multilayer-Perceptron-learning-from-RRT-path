#!/usr/bin/env python3
import os
import re
import pandas as pd

class extract_middle:
    def __init__(self):
        self.input_df1 = pd.DataFrame()
        self.input_df2 = pd.DataFrame()
        self.input_df3 = pd.DataFrame()
        self.all_df = pd.DataFrame()
        self.test_df = pd.DataFrame()

        self.s_df = pd.DataFrame()
        self.g_df = pd.DataFrame()
        self.ma_df = pd.DataFrame()
        self.mb_df = pd.DataFrame()
        self.mc_df = pd.DataFrame()
        self.ts_df = pd.DataFrame()
        self.tg_df = pd.DataFrame()

        self.columns_s = [f's{i+1}' for i in range(6)]
        self.columns_g = [f'g{i+1}' for i in range(6)]
        self.columns_ma = [f'ma{i+1}' for i in range(6)]
        self.columns_mb = [f'mb{i+1}' for i in range(6)]
        self.columns_mc = [f'mc{i+1}' for i in range(6)]

    def middle_index(self, matches) : 
        if matches % 2 == 0: 
            middle_index = matches // 2 - 1
        else:
            middle_index = matches // 2
        return middle_index

    def extract_middle(self, learning_folder):
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
                        middleA_index = self.middle_index(len(matches))
                        middleB_index = self.middle_index(middleA_index)
                        middleC_index = middleA_index+middleB_index
                        
                        start = [eval(matches[0].replace(']', ']'))]
                        middleA = [eval(matches[middleA_index].replace(']', ']'))]
                        middleB = [eval(matches[middleB_index].replace(']', ']'))]
                        middleC = [eval(matches[middleC_index].replace(']', ']'))]
                        goal = [eval(matches[-1].replace(']', ']'))]

                        # 각각의 DataFrame에 추가
                        self.s_df = pd.concat([self.s_df, pd.DataFrame(data=start, columns=self.columns_s)])
                        self.g_df = pd.concat([self.g_df, pd.DataFrame(data=goal, columns=self.columns_g)])
                        self.ma_df = pd.concat([self.ma_df, pd.DataFrame(data=middleA, columns=self.columns_ma)])
                        self.mb_df = pd.concat([self.mb_df, pd.DataFrame(data=middleB, columns=self.columns_mb)])
                        self.mc_df = pd.concat([self.mc_df, pd.DataFrame(data=middleC, columns=self.columns_mc)])

    def extract_sg(self, test_folder):
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
                        self.ts_df = pd.concat([self.ts_df, pd.DataFrame(data=start, columns=self.columns_s)])
                        self.tg_df = pd.concat([self.tg_df, pd.DataFrame(data=goal, columns=self.columns_g)])


    def save_to_csv(self, learning_folder, test_folder, output_path):
        self.extract_middle(learning_folder)
        
        # # start, middleB, middleA
        # self.input_df1 = pd.concat([self.s_df, self.g_df], axis=1)
        # self.input_df1.to_csv(os.path.join(output_path, 'input1.csv'), index=False)
        # self.ma_df.to_csv(os.path.join(output_path, 'output1.csv'), index=False)

        # # start, middleA, goal
        # self.input_df2 = pd.concat([self.s_df, self.ma_df], axis=1)
        # self.input_df2.to_csv(os.path.join(output_path, 'input2.csv'), index=False)
        # self.mb_df.to_csv(os.path.join(output_path, 'output2.csv'), index=False)

        # # middleA, middleC, goal
        # self.input_df3 = pd.concat([self.ma_df, self.g_df], axis=1)
        # self.input_df3.to_csv(os.path.join(output_path, 'input3.csv'), index=False)
        # self.mc_df.to_csv(os.path.join(output_path, 'output3.csv'), index=False)

        # all Dataset
        self.all_df = pd.concat([self.s_df, self.mb_df, self.ma_df, self.mc_df, self.g_df], axis=1)
        self.all_df.to_csv(os.path.join(output_path, 'all.csv'), index=False)

        # # TEST Dataset
        # self.extract_sg(test_folder)
        # # start, goal
        # self.test_df = pd.concat([self.ts_df, self.tg_df], axis=1)
        # self.test_df.to_csv(os.path.join(output_path, 'testinput.csv'), index=False)

# angle 폴더 내의 모든 파일에 대해 반복
default_folder = '/home/nishidalab07/github/6dimension/simulation2'

input_folder_path = os.path.join(default_folder, 'Configuration/originpath/sample')
# input_folder_path = os.path.join(default_folder, 'Configuration/selected_op')
test_folder_path = os.path.join(default_folder, 'Configuration/test')
output_folder_path = os.path.join(default_folder, 'csv') 

extractor = extract_middle()
extractor.save_to_csv(input_folder_path, test_folder_path, output_folder_path)
