class Devide:
    def devide(self, input_file_path, output_file_path, chunk_size):
        # Read the input file
        with open(input_file_path, 'r') as input_file:
            lines = input_file.readlines()

        # Split the lines into chunks
        chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

        # Write chunks to separate output files
        for i, chunk in enumerate(chunks):
            output_filename = f'{output_file_path}/path_{i + 1}.txt'
            with open(output_filename, 'w') as output_file:
                output_file.writelines(chunk)

# input_file_path = '/home/nishidalab07/github/6dimension/new_simulation/extract_train_C/sg.txt'
# output_file_path = '/home/nishidalab07/github/6dimension/new_simulation/extract_train_C/sgpath'
# Devide.devide(input_file_path, output_file_path)
