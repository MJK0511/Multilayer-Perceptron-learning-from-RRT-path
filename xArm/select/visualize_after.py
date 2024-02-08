import os
import pandas as pd
from plot import Plot

class MakeDF:
    def __init__(self):
        self.m_df = pd.DataFrame()
        self.columns = ['sx', 'sy', 'sz', 'mbx', 'mby', 'mbz', 'max', 'may', 'maz', 'mcx', 'mcy', 'mcz', 'gx', 'gy', 'gz']

    def makedf(self, learning_folder):
        for filename in os.listdir(learning_folder):
            if filename.endswith('.txt'):
                file_path = os.path.join(learning_folder, filename)

                with open(file_path, 'r') as file:
                    data = file.readlines()

                    # 데이터를 DataFrame에 추가
                    s = list(map(float, data[0].strip('[]').split(',')[:3]))
                    mb = list(map(float, data[1].strip('[]').split(',')[:3]))
                    ma = list(map(float, data[2].strip('[]').split(',')[:3]))
                    mc = list(map(float, data[3].strip('[]').split(',')[:3]))
                    g = list(map(float, data[4].strip('[]').split(',')[:3]))

                    # 데이터를 DataFrame에 추가
                    row_data = s + mb + ma + mc + g
                    self.m_df = pd.concat([self.m_df, pd.DataFrame([row_data], columns=self.columns)], ignore_index=True)

if __name__ == "__main__":
    plotter = Plot()
    makedf = MakeDF()

    default_path = "/home/nishidalab07/github/6dimension/new_simulation/"
    input_directory = os.path.join(default_path, 'Task/After_train/allpath')
    makedf.makedf(input_directory)
    plotter.plot_2d_all(makedf.m_df)
