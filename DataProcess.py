import os
import pandas as pd
def process_csv(input_path, output_path):
    # 입력 디렉토리에서 모든 CSV 파일 목록 가져오기
    csv_files = [f for f in os.listdir(input_path) if f.endswith('.csv')]

    # 빈 데이터프레임 생성
    combined_input_df = pd.DataFrame()
    combined_output_df = pd.DataFrame()

    for csv_file in csv_files:
        # CSV 파일의 전체 경로
        file_path = os.path.join(input_path, csv_file)

        # CSV 파일을 DataFrame으로 읽기
        df = pd.read_csv(file_path)

        # 첫 번째, 중간, 마지막 값 추출
        start = df.iloc[0]
        middle_index = len(df) // 2
        middle_value = df.iloc[middle_index] if len(df) % 2 == 1 else df.iloc[middle_index - 1]
        goal = df.iloc[-1]

        # 추출한 값들로 새로운 DataFrame 생성
        input_df = pd.DataFrame({
            'sx': [start[1]],
            'sy': [start[0]],
            'gx': [goal[1]],
            'gy': [goal[0]]
        })
        # 결과를 빈 데이터프레임에 추가
        combined_input_df = pd.concat([combined_input_df, input_df], ignore_index=True)

        # 추출한 값들로 새로운 DataFrame 생성
        output_df = pd.DataFrame({
            'mx': [middle_value[1]],
            'my': [middle_value[0]],
        })
        # 결과를 빈 데이터프레임에 추가
        combined_output_df = pd.concat([combined_output_df, output_df], ignore_index=True)

    # 모든 데이터를 하나의 CSV 파일로 저장
    #input data
    input_data_file = os.path.join(output_path, 'test_input_data.csv')
    combined_input_df.to_csv(input_data_file, index=False)
    #output data
    output_data_file = os.path.join(output_path, 'test_output_data.csv')
    combined_output_df.to_csv(output_data_file, index=False)

if __name__ == "__main__":
    # 입력 디렉토리와 출력 디렉토리 설정
    input_directory = r'C:\MJ\github\RRT_path\test'
    output_directory = r'C:\MJ\github\test_path'

    # 프로세스 실행
    process_csv(input_directory, output_directory)
