import os
import re

class extract_C_all:
    def process_file(self, input_file_path, output_folder_path):
        with open(input_file_path, 'r') as file:
            data = file.read()
            pattern = r'positions:\s*(\[.*?\])'
            matches = re.findall(pattern, data)

            result_text = '\n'.join(match.replace(']', ']') for match in matches)

            # save
            filename = os.path.basename(input_file_path)
            result_file_path = os.path.join(output_folder_path, filename.replace('.txt', '_R.txt'))
            with open(result_file_path, 'w') as result_file:
                result_file.write(result_text)

            print(f"Results saved to {result_file_path}")

    def process_files_in_directory(self, input_folder_path, output_folder_path):
        for filename in os.listdir(input_folder_path):
            if filename.endswith('.txt'):
                input_file_path = os.path.join(input_folder_path, filename)
                self.process_file(input_file_path, output_folder_path)

# if __name__ == "__main__":
#     default_folder = '/home/nishidalab07/github/6dimension/simulation2'
#     extractor = extract_C_all()
#     # RRT path로부터 모든 positions를 추출 
#     input_folder_path = os.path.join(default_folder, 'Configuration/originpath/test')
#     output_folder_path = os.path.join(default_folder, 'Configuration/extract_angle')
#     extractor.process_files_in_directory(input_folder_path, output_folder_path)