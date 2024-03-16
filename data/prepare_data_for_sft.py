import os
import json

def consolidate_json_files(source_directory, output_file):
    consolidated_data = []
    error_files = []

    for file_name in os.listdir(source_directory):
        if file_name.endswith('.txt'):  # Assuming all your files are .txt
            file_path = os.path.join(source_directory, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    consolidated_data.append(data)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"Error processing {file_name}: {e}")
                error_files.append(file_name)

    # Writing the consolidated JSON data to a file
    with open(output_file, 'w', encoding='utf-8') as output:
        json.dump(consolidated_data, output, indent=4)

    return error_files

if __name__ == "__main__":
    source_directory = 'data/gpt4gen/'
    output_file = 'data/generated_data.json'

    error_files = consolidate_json_files(source_directory, output_file)
    if error_files:
        print("Some files were not processed successfully:", error_files)
    else:
        print("All files have been consolidated successfully.")
