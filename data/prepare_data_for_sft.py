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

def add_instruction_to_json(input_file, output_file=None):
    if not output_file:
        output_file = input_file  # Modify the original file if no output file is specified

    instruction_text = ("Create a list of chords,a corresponding scale to improve with, title, and style along with an example in ABC notation based on this input in JSON format.")

    # Read the original JSON data
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Error reading {input_file}: {e}")
        return

    # Modify each item in the list
    modified_data = [
        {
            "instruction": instruction_text,
            "input": item.get("input", ""),  # Use the existing input
            "output": item.get("output", {})  # Use the existing output
        } for item in data
    ]

    # Write the modified data to the output file
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(modified_data, file, indent=4)
        print(f"Successfully modified and saved to {output_file}.")
    except IOError as e:
        print(f"Error writing to {output_file}: {e}")

def modify_output_to_string(input_file, output_file):
    # Load the JSON data from the input file
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Error reading {input_file}: {e}")
        return

    # Modify the 'output' field in each entry to be a JSON string
    for entry in data:
        if 'output' in entry:
            entry['output'] = json.dumps(entry['output'], ensure_ascii=False)

    # Write the modified data back to the output file
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Successfully modified and saved to {output_file}.")
    except IOError as e:
        print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    # source_directory = 'data/gpt4gen/'
    # output_file = 'data/generated_data.json'

    # error_files = consolidate_json_files(source_directory, output_file)
    # if error_files:
    #     print("Some files were not processed successfully:", error_files)
    # else:
    #     print("All files have been consolidated successfully.")

    # add instruction
    input_file = 'data/sft_data.json'
    output_file = 'data/sft_data_string.json'  
    modify_output_to_string(input_file, output_file)
