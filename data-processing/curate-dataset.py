import datetime
import os
from sklearn.model_selection import train_test_split

script_dir = os.path.dirname(os.path.abspath(__file__))
repo_dir = os.path.normpath(os.path.join(script_dir, '..', 'data-bal-files')) # Adjust this path to your repo location
output_dir = os.path.normpath(os.path.join(script_dir, '..', 'data', 'raw'))   # Adjust this path to your output location

# Get the current date and time
current_date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

dataset_output_file = f'dataset_{current_date_time}.txt'
train_output_file = f'train_{current_date_time}.txt'
val_output_file = f'val_{current_date_time}.txt'
test_output_file = f'test_{current_date_time}.txt'
enable_train_val_test_split = False  # Set to False if you don't want to split into train/val/test

if i:=input(f"""
Source directory: {repo_dir}
Output directory: {output_dir}
train_val_test split: {enable_train_val_test_split}

Proceed? (y/n): """).strip().lower() == 'y':
    pass
else:
    print("Exiting...")
    exit(0)


# Variables for train/val/test split\
train_size = 0.8  # 80% for training
val_size = 0.1    # 10% for validation
test_size = 0.1   # 10% for testing

# Set the random seed for reproducibility
random_seed = 42

# Check if the sizes are valid
if not (0 <= train_size <= 1 and 0 <= test_size <= 1 and 0 <= val_size <= 1):
    raise ValueError("Sizes must be between 0 and 1.")
if round(train_size + test_size + val_size, 10) != 1.0:  # Handling floating-point precision issues
    raise ValueError("Train, test, and validation sizes must add up to 1.")

# Set the random seed for train_test_split
import random
random.seed(random_seed)
import numpy as np
np.random.seed(random_seed)

# Check if the directory exists
if not os.path.exists(repo_dir):
    raise FileNotFoundError(f"The directory {repo_dir} does not exist.")

# Check if the directory is empty
if not os.listdir(repo_dir):
    raise ValueError(f"The directory {repo_dir} is empty.")

# Check if the output directory exists, if not create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Collect all .bal files
print("=== Collecting all .bal files ===")
bal_files = []
for root, dirs, files in os.walk(repo_dir):
    for file in files:
        if file.endswith('.bal'):
            bal_files.append(os.path.join(root, file))
print(f"Total .bal files found: {len(bal_files)}")
print("=== Finished collecting .bal files ===")

print("=== Balancing the dataset ===")
# Split into train, validation, and test sets if enabled
if enable_train_val_test_split:
    # Ensure the files are balanced across the splits
    train_files, temp_files = train_test_split(bal_files, train_size=train_size, random_state=random_seed)
    val_files, test_files = train_test_split(temp_files, test_size=test_size/(test_size + val_size), random_state=random_seed)
else:
    # If not splitting, just use all files for training
    train_files = bal_files
    val_files = []
    test_files = []

# Function to read file contents
def read_files(file_list):
    return [open(file, 'r', encoding='utf-8').read() for file in file_list]

# Prepare the datasets
print("=== Reading the dataset files ===")
train_data = read_files(train_files)
val_data = read_files(val_files)
test_data = read_files(test_files)
print("=== Finished reading the dataset files ===")

if enable_train_val_test_split:
    print(f"Training files: {len(train_files)}, Validation files: {len(val_files)}, Test files: {len(test_files)}")
else:
    print(f"Dataset files: {len(train_files)}")

print("=== Started writing the dataset ===")
if enable_train_val_test_split:
    # Save the datasets to text files
    with open(os.path.join(output_dir, train_output_file), 'w', encoding='utf-8') as f:
        f.write('\n'.join(train_data))
    with open(os.path.join(output_dir, val_output_file), 'w', encoding='utf-8') as f:
        f.write('\n'.join(val_data))
    with open(os.path.join(output_dir, test_output_file), 'w', encoding='utf-8') as f:
        f.write('\n'.join(test_data))
else:
    # Save the dataset to a single text file
    with open(os.path.join(output_dir, dataset_output_file), 'w', encoding='utf-8') as f:
        f.write('\n'.join(train_data))
print("=== Finished writing the dataset ===")
    