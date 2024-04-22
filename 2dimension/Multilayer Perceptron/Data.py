import os
import pandas as pd

class call_LD():
    def __init__(self, infilename, outfilename):
        # train_directory = r"C:\MJ\github\training_path"
        train_directory = r"/home/nishidalab07/github/training_path"
        train_file_path = os.path.join(train_directory, infilename)
        self.train_input_data = pd.read_csv(train_file_path)
        self.train_input_data = self.train_input_data[['sx', 'sy', 'gx', 'gy']]

        train_file_path = os.path.join(train_directory, outfilename)
        self.train_output_data = pd.read_csv(train_file_path)
        self.train_output_data = self.train_output_data[['mx', 'my',]]
    
class call_TD():
    def __init__(self, infilename):
        # test_directory = r"C:\MJ\github\test_path"
        test_directory = r"/home/nishidalab07/github/test_path"
        test_file_path = os.path.join(test_directory, infilename)
        self.test_data = pd.read_csv(test_file_path)
        self.test_data = self.test_data[['sx', 'sy', 'gx', 'gy']].values
        