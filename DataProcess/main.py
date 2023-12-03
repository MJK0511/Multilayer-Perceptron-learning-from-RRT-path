from DataProcess import ProcessCSV

if __name__ == "__main__":
    # Input directory and output directory settings
    input_directory = r'/home/nishidalab07/github/RRT_path/test'
    output_directory = r'/home/nishidalab07/github/test_path'

    input_filename = 'test_input_data.csv'
    output_filename = 'test_output_data.csv'

    # Create an instance of the ProcessCSV class
    processor = ProcessCSV(input_directory, output_directory)

    # Call the method to process the CSV files
    processor.process_csv_files(input_filename, output_filename)