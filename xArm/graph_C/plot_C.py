import matplotlib.pyplot as plt
import os
import pandas as pd 

class Plot_C():
    def plot_2d_all(self, df):
        # 각각의 2차원 그래프를 그릴 서브플롯 생성
        n = 5
        fig, axs = plt.subplots(1, 5, figsize=(20, 5))  # Changed the number of subplots to 5

        for i in range(n):
            self.plot_2d(axs[i], df, i+1, i+2)

        # 전체 그래프 제목
        fig.suptitle('2D Plots')

        plt.show()

    def plot_2d(self, ax, df, joint1, joint2):
        # ax.plot([df[f's{joint1}'], df[f'ma{joint1}'], df[f'g{joint1}']],
        #         [df[f's{joint2}'], df[f'ma{joint2}'], df[f'g{joint2}']],
        #         marker='o', color='gray')
        ax.scatter(df[f'ma{joint1}'], df[f'ma{joint2}'], marker='o', color='gray', s=100)  # only midpoint, scatter 함수로 변경
        ax.set_xlabel(f'joint{joint1}')
        ax.set_ylabel(f'joint{joint2}')
        ax.set_title(f'joint{joint1}, joint{joint2} plane')

if __name__ == "__main__":
    plotter = Plot_C()
    default_path = "/home/nishidalab07/github/6dimension/simulation1/"
    
    input_file_path = os.path.join(default_path, 'csv/sample.csv')  # Fixed the input file path
    output_directory = default_path

    # Read the CSV file into a DataFrame (df)
    df = pd.read_csv(input_file_path)

    # Plot all 2D graphs using the provided method
    plotter.plot_2d_all(df)