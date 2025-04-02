import json
import os
import re
from pprint import pprint

from utils import get_most_recent_file_with_prefix

script_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.normpath(os.path.join(script_dir, '..', 'data', 'raw')) # Adjust this path to your repo location
output_dir = os.path.normpath(os.path.join(script_dir, '..', 'data', 'block-formatted'))   # Adjust this path to your output location
chatML_dir = os.path.normpath(os.path.join(script_dir, '..', 'data', 'chatML'))   # Adjust this path to your output location    

enable_train_val_test_split = False  # Set to False if you don't want to split into train/val/test

if i:=input(f"""
Source directory: {source_dir}
Output directory: {output_dir}
train_val_test split: {enable_train_val_test_split}

Proceed? (y/n): """).strip().lower() == 'y':
    pass
else:
    print("Exiting...")
    exit(0)

# Check if the directory exists
if not os.path.exists(source_dir):
    raise FileNotFoundError(f"The directory {source_dir} does not exist.")

# Check if the directory is empty
if not os.listdir(source_dir):
    raise ValueError(f"The directory {source_dir} is empty.")

# Check if the output directory exists, if not create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Check if the chatML directory exists, if not create it
if not os.path.exists(chatML_dir):
    os.makedirs(chatML_dir)

# Load the most recent dataset file paths
print("=== Loading the most recent dataset files ===")
dataset_input_file = get_most_recent_file_with_prefix(source_dir, 'dataset_')
train_input_file = get_most_recent_file_with_prefix(source_dir, 'train_')
val_input_file = get_most_recent_file_with_prefix(source_dir, 'val_')
test_input_file = get_most_recent_file_with_prefix(source_dir, 'test_')

# Check for the presence of the dataset files
if enable_train_val_test_split and not (train_input_file and val_input_file and test_input_file):
    raise ValueError("Train, validation, and test files are required for splitting.")
if not enable_train_val_test_split and not dataset_input_file:
    raise ValueError("Dataset file is required for processing.")

def extract_code_blocks(content):
    """Extract individual code blocks (e.g., functions) from a Ballerina code string."""

    # Regex to match Ballerina function definitions
    # Matches: 'function name(params) returns type { ... }'
    function_pattern = r'function\s+\w+\s*\([^)]*\)\s*(?:returns\s+\w+)?\s*\{[^}]*\}'

    # Matches: 'service name on host { ... }'
    service_pattern = r'service\s+\w+\s+on\s+\w+\s*\{[^}]*\}'

    # Combine the patterns to match both functions and services
    combined_pattern = f"({function_pattern}|{service_pattern})"

    # Match combined
    blocks = re.findall(combined_pattern, content, re.DOTALL)
    return blocks

def create_completion_pairs(code_blocks):
    """Generate input-output pairs for code completion."""
    pairs = []
    for block in code_blocks:
        lines = block.split('\n')
        # Take the first 1-2 lines as partial code (input)
        partial_code = '\n'.join(lines[:1]).strip()
        full_code = block.strip()
        pairs.append({
            "input": partial_code,
            "output": full_code
        })
    return pairs

def format_chatml(pairs, output_file):
    """Convert input-output pairs to ChatML format and save as JSONL."""
    with open(output_file, 'w') as f:
        for pair in pairs:
            chatml_entry = {
                "messages": [
                    {"role": "system", "content": "You are a Ballerina code completion assistant."},
                    {"role": "user", "content": f"Complete this Ballerina code:\n```ballerina\n{pair['input']}\n```"},
                    {"role": "assistant", "content": f"```ballerina\n{pair['output']}\n```"}
                ]
            }
            f.write(json.dumps(chatml_entry) + '\n')

print("=== Extracting code blocks ===")
if enable_train_val_test_split:
    # Load the train, validation, and test files
    with open(train_input_file, 'r', encoding='utf-8') as f:
        train_data = f.read()
    with open(val_input_file, 'r', encoding='utf-8') as f:
        val_data = f.read()
    with open(test_input_file, 'r', encoding='utf-8') as f:
        test_data = f.read()

    raise NotImplementedError("Train, validation, and test files handling are not yet implemented.")
else:
    # Load the dataset file
    with open(dataset_input_file, 'r', encoding='utf-8') as f:
        all_data = f.read()
        all_data_blocks = extract_code_blocks(all_data)

        print(f"Total code blocks found: {len(all_data_blocks)}")

    # Save the extracted code blocks to a new file
    print("=== Writing the extracted code blocks to file ===")    
    output_file = os.path.join(output_dir, f'blocks_{os.path.basename(dataset_input_file)}.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_data_blocks))
    print("=== Finished writing code blocks ===")

    input_output_pairs = create_completion_pairs(all_data_blocks)
    print(f"Total input-output pairs created: {len(input_output_pairs)}")

    # Save the input-output pairs to a new file
    print("=== Writing the input-output pairs to file ===")
    json_output_file = os.path.join(chatML_dir, f'chat_{os.path.basename(dataset_input_file)}.jsonl')
    format_chatml(input_output_pairs, json_output_file)
    print("=== Finished writing input-output pairs ===")






# # Collect all .bal files
# print("=== Collecting all .bal files ===")
# bal_files = []
# for root, dirs, files in os.walk(repo_dir):
#     for file in files:
#         if file.endswith('.bal'):
#             bal_files.append(os.path.join(root, file))
# print(f"Total .bal files found: {len(bal_files)}")
# print("=== Finished collecting .bal files ===")

# print("=== Balancing the dataset ===")
# # Split into train, validation, and test sets if enabled
# if enable_train_val_test_split:
#     # Ensure the files are balanced across the splits
#     train_files, temp_files = train_test_split(bal_files, train_size=train_size, random_state=random_seed)
#     val_files, test_files = train_test_split(temp_files, test_size=test_size/(test_size + val_size), random_state=random_seed)
# else:
#     # If not splitting, just use all files for training
#     train_files = bal_files
#     val_files = []
#     test_files = []

# # Function to read file contents
# def read_files(file_list):
#     return [open(file, 'r', encoding='utf-8').read() for file in file_list]

# # Prepare the datasets
# print("=== Reading the dataset files ===")
# train_data = read_files(train_files)
# val_data = read_files(val_files)
# test_data = read_files(test_files)
# print("=== Finished reading the dataset files ===")

# if enable_train_val_test_split:
#     print(f"Training files: {len(train_files)}, Validation files: {len(val_files)}, Test files: {len(test_files)}")
# else:
#     print(f"Dataset files: {len(train_files)}")

# print("=== Started writing the dataset ===")
# if enable_train_val_test_split:
#     # Save the datasets to text files
#     with open(os.path.join(output_dir, train_output_file), 'w', encoding='utf-8') as f:
#         f.write('\n'.join(train_data))
#     with open(os.path.join(output_dir, val_output_file), 'w', encoding='utf-8') as f:
#         f.write('\n'.join(val_data))
#     with open(os.path.join(output_dir, test_output_file), 'w', encoding='utf-8') as f:
#         f.write('\n'.join(test_data))
# else:
#     # Save the dataset to a single text file
#     with open(os.path.join(output_dir, dataset_output_file), 'w', encoding='utf-8') as f:
#         f.write('\n'.join(train_data))
# print("=== Finished writing the dataset ===")
    