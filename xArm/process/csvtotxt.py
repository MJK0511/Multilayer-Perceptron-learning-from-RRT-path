import pandas as pd

# CSV 파일 불러오기
# csv_file_path = '/home/nishidalab07/github/6dimension/new_simulation/after/testinput.csv'
# output_file_path = '/home/nishidalab07/github/6dimension/new_simulation/extract_train_C/sg.txt'

class csvtotxt:
    def csv_to_txt(self, csv_file_path, output_file_path):
        # angle.txt 파일 생성
        df = pd.read_csv(csv_file_path, header=None)
        with open(output_file_path, 'w') as output_file:
            # 데이터 프레임의 행 수만큼 반복
            for i in range(1, len(df)):
                # 데이터 프레임의 열 수만큼 반복
                for j in range(0, len(df.columns), 6):
                    # 각 행을 선택하여 출력
                    row_values = df.iloc[i, j:j+6].values.tolist()
                    formatted_values = f"[{', '.join(map(str, row_values))}]"
                    output_file.write(formatted_values + '\n')
