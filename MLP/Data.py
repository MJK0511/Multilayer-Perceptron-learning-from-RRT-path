import os
import pandas as pd

class TrainingData():
    def __init__(self):
        # CSVファイルのディレクトリー
        train_directory = '/home/nishidalab07/github/RRT/training_path/'

        # ディレクトリーのすべてのファイルとディレクトリーリストを得る
        all_files = os.listdir(train_directory)
        train_file_paths = [os.path.join(train_directory, file_name) for file_name in all_files if file_name.endswith('.csv')]
        self.all_train_data = pd.DataFrame() # 読み込んだデータを入れるDataFrame
        
        # すべてのCSVファイルを読み込み、一つのDataFrameにする
        for train_file_path in train_file_paths:
            train_data = pd.read_csv(train_file_path)
            # 転置して列名変更
            train_data = train_data.T.rename(columns={0: 's', 1: 'm1', 2: 'm2', 3: 'm3', 4: 'm4', 5: 'm5', 6: 'm6', 7:'g'})
            #
            self.all_train_data = pd.concat([self.all_train_data, train_data], ignore_index=True)
            
            
        # 'Y'と'X'X列だけ選択
        self.all_train_data = self.all_train_data[['s', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'g']]


class TestData():
    def __init__(self):
        test_directory = '/home/nishidalab07/github/RRT/test_path/'
        test_file_path = os.path.join(test_directory, 'Test.csv')
        self.test_data = pd.read_csv(test_file_path)
        self.test_data = self.test_data.T.rename(columns={0: 's', 1: 'm1', 2: 'm2', 3: 'm3', 4: 'm4', 5: 'm5', 6: 'm6', 7:'g'})
        # データ設定    
        self.test_input = self.test_data[['s', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'g']].values
    

