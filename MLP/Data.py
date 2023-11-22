import os
import pandas as pd

class TrainingData():
    def __init__(self):
        # CSVファイルのディレクトリー
        train_directory = 'C:/MJ/github/training_path/'

        # ディレクトリーのすべてのファイルとディレクトリーリストを得る
        all_files = os.listdir(train_directory)

        # CSV　ファイルのパスを生成
        train_file_paths = [os.path.join(train_directory, file_name) for file_name in all_files if file_name.endswith('.csv')]

        # 読み込んだデータを入れるDataFrame
        self.all_train_data = pd.DataFrame()

        # すべてのCSVファイルを読み込み、一つのDataFrameにする
        for train_file_path in train_file_paths:
            train_data = pd.read_csv(train_file_path)
            self.all_train_data = pd.concat([self.all_train_data, train_data], ignore_index=True)

        # 'Y'와 'X' 열만 선택
        self.all_train_data = self.all_train_data[['Y', 'X']]

# traindata_instance = TrainingData()
# print(traindata_instance.all_train_data)

class TestData():
    def __init__(self):
        test_directory = 'C:/MJ/github/test_path/'
        test_file_path = os.path.join(test_directory, 'coordinates_f20231121183359.csv')

        # テストデータCSVファイル読み込み
        self.test_data = pd.read_csv(test_file_path)

        # データ設定    
        self.test_input = self.test_data[['Y', 'X']].values
    

