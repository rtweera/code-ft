import os
from sklearn.model_selection import train_test_split

# Directory containing all Ballerina repos
repo_dir = 'initial-data'  # Adjust this path to your repo location
cwd = os.getcwd()
os.chdir(cwd)

# Collect all .bal files
bal_files = []
for root, dirs, files in os.walk(repo_dir):
    for file in files:
        if file.endswith('.bal'):
            bal_files.append(os.path.join(root, file))
print(f"Total .bal files found: {len(bal_files)}")

# Split into train (80%), validation (10%), and test (10%)
train_files, temp_files = train_test_split(bal_files, test_size=0.2, random_state=42)
val_files, test_files = train_test_split(temp_files, test_size=0.5, random_state=42)

# Function to read file contents
def read_files(file_list):
    return [open(file, 'r', encoding='utf-8').read() for file in file_list]

# Prepare the datasets
train_data = read_files(train_files)
val_data = read_files(val_files)
test_data = read_files(test_files)

print(f"Training files: {len(train_files)}, Validation files: {len(val_files)}, Test files: {len(test_files)}")

# Save the datasets to text files
with open('train.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(train_data))
with open('val.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(val_data))
with open('test.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(test_data))
    