import os
import pandas as pd

class ProcessCSV:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.combined_input_df = pd.DataFrame()
        self.combined_output_df = pd.DataFrame()

    def process_csv_files(self, filename1, filename2):
        csv_files = [f for f in os.listdir(self.input_path) if f.endswith('.csv')]

        for csv_file in csv_files:
            file_path = os.path.join(self.input_path, csv_file)
            df = pd.read_csv(file_path)

            # Extract information from the DataFrame
            start, middle_value, goal = self.extract_middle1(df)  ### ここを修正して抽出する中点を変える

            # Create new DataFrames
            input_df = self.create_input_dataframe(start, goal)
            output_df = self.create_output_dataframe(middle_value)

            # Append to combined DataFrames
            self.combined_input_df = pd.concat([self.combined_input_df, input_df], ignore_index=True)
            self.combined_output_df = pd.concat([self.combined_output_df, output_df], ignore_index=True)

        # Save combined DataFrames to CSV
        self.save_to_csv(filename1, filename2)
    
    # 始点 m1 終点
    def extract_middle1(self, df):
        start = df.iloc[0]
        middle_index = len(df) // 2
        middle_value = df.iloc[middle_index] if len(df) % 2 == 1 else df.iloc[middle_index - 1]
        goal = df.iloc[-1]
        return start, middle_value, goal
    
    # 始点 m2 m1
    def extract_middle2(self, df):
        start = df.iloc[0]
        middle_index1 = len(df) // 2
        middle_index2 = middle_index1 // 2
        middle_value = df.iloc[middle_index2] if len(df) % 2 == 1 else df.iloc[middle_index2 - 1]
        goal = df.iloc[middle_index1] if len(df) % 2 == 1 else df.iloc[middle_index1 - 1]
        return start, middle_value, goal
    
    # m1 m3 終点
    def extract_middle3(self, df):
        middle_index1 = len(df) // 2
        start = df.iloc[middle_index1] if len(df) % 2 == 1 else df.iloc[middle_index1 - 1]
        middle_index3 = middle_index1 + (middle_index1//2)
        middle_value = df.iloc[middle_index3] if len(df) % 2 == 1 else df.iloc[middle_index3 - 1]
        goal = df.iloc[-1]
        return start, middle_value, goal
         
    def create_input_dataframe(self, start, goal):
        return pd.DataFrame({
            'sx': [start[1]],
            'sy': [start[0]],
            'gx': [goal[1]],
            'gy': [goal[0]]
        })

    def create_output_dataframe(self, middle_value):
        return pd.DataFrame({
            'mx': [middle_value[1]],
            'my': [middle_value[0]],
        })

    def save_to_csv(self, filename1, filename2):
        input_data_file = os.path.join(self.output_path, filename1)
        self.combined_input_df.to_csv(input_data_file, index=False)

        output_data_file = os.path.join(self.output_path, filename2)
        self.combined_output_df.to_csv(output_data_file, index=False)