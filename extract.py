import json
import chardet

def empty_values(obj):
    if isinstance(obj, dict):
        return {k: empty_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [empty_values(item) for item in obj]
    else:
        return None

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        return chardet.detect(raw_data)['encoding']

def read_json_file(file_path):
    encoding = detect_encoding(file_path)
    print(f"Detected encoding: {encoding}")
    
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return json.load(file)
    except UnicodeDecodeError:
        print(f"Failed to decode with {encoding}, trying with utf-8")
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return None

# Specify your input JSON file path
input_file_path = 'dataset/about.json'

# Read the JSON file
data = read_json_file(input_file_path)

if data is not None:
    # Create a new structure with empty values
    empty_data = empty_values(data)

    # Write the new structure to a JSON file
    output_file_path = 'keys_only.json'
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(empty_data, output_file, indent=2)

    print(f"JSON structure with empty values has been saved to '{output_file_path}'")
else:
    print("Failed to process the JSON file.")
