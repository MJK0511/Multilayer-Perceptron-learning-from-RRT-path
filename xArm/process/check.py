import os
import csv
class Check:
    def count_positions_in_file(self, file_path):
        try:    
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content.lower().count('positions')
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return 0

    def process_directory(self, directory_path, output_csv_path):
        result_data = []
        
        # Iterate through all files in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory_path, filename)
                positions_count = self.count_positions_in_file(file_path)
                result_data.append({'filename': filename, 'count': positions_count})
        
        # Save results to CSV
        csv_columns = ['filename', 'count']
        csv_file_path = os.path.join(output_csv_path)
        
        try:
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
                writer.writeheader()
                for data in result_data:
                    writer.writerow(data)
            print(f"Results saved to {csv_file_path}")
        except Exception as e:
            print(f"Error writing to CSV file: {e}")        

# if __name__ == "__main__":
#     # Specify the input directory and output directory
#     input_directory = '/home/nishidalab07/github/6dimension/new_simulation/origin_path/training'
#     output_directory = '/home/nishidalab07/github/6dimension/new_simulation'
    
#     # Process the directory and save results to CSV
#     Check.process_directory(input_directory, output_directory)
