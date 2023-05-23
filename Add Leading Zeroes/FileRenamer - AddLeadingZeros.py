import os
import re

def get_script_directory():
    return os.path.dirname(os.path.abspath(__file__))

directory = get_script_directory()

def is_incorrect_format(filename):
    pattern = re.compile(r'^\d{1,2}_.+$')
    return bool(pattern.match(filename))

for file in os.listdir(directory):
    file_path = os.path.join(directory, file)
    if os.path.isfile(file_path) and is_incorrect_format(file):
        # Extract the number from the file name and pad it with zeros
        number_part = re.match(r'\d+', file).group()
        padded_number = str(int(number_part)).zfill(3)
        
        # Replace the old number with the new padded number
        new_file_name = file.replace(number_part, padded_number)
        new_file_path = os.path.join(directory, new_file_name)
        os.rename(file_path, new_file_path)

        # Print information about the renaming process
        print(f"Renamed '{file}' to '{new_file_name}'")
