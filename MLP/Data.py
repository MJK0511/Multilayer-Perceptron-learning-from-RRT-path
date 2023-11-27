import os
import pandas as pd

class TrainingData():
    def __init__(self):
        # CSVファイルのディレクトリー
        train_directory = r"C:\MJ\github\training_path"
        train_file_path = os.path.join(train_directory, 'training_input_data.csv')
        self.train_input_data = pd.read_csv(train_file_path)
        self.train_input_data = self.train_input_data[['sx', 'sy', 'gx', 'gy']]

        train_file_path = os.path.join(train_directory, 'training_output_data.csv')
        self.train_output_data = pd.read_csv(train_file_path)
        self.train_output_data = self.train_output_data[['mx', 'my',]]
       
class TestData():
    def __init__(self):
        test_directory = r"C:\MJ\github\test_path"
        test_file_path = os.path.join(test_directory, 'test_input_data.csv')
        self.test_data = pd.read_csv(test_file_path)
        self.test_input = self.test_data[['sx', 'sy', 'gx', 'gy']].values
