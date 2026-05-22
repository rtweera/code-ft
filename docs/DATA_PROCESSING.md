# Data Processing Guide

Complete guide to preparing and processing Ballerina code datasets for model training.

## Table of Contents

1. [Overview](#overview)
2. [Data Sources](#data-sources)
3. [Dataset Curation](#dataset-curation)
4. [Dataset Formatting](#dataset-formatting)
5. [Supported Formats](#supported-formats)
6. [Advanced Usage](#advanced-usage)
7. [Troubleshooting](#troubleshooting)

## Overview

The data processing pipeline transforms raw Ballerina code into training-ready datasets through two main stages:

1. **Curation**: Extract code snippets from `.bal` files
2. **Formatting**: Convert to training formats (ChatML, Block)

## Data Sources

### Input Requirements

The project expects Ballerina code in `.bal` files organized in a directory structure:

```
data-bal-files/
├── module1/
│   ├── main.bal
│   ├── utils.bal
│   └── types.bal
├── module2/
│   ├── service.bal
│   └── client.bal
└── examples/
    ├── hello_world.bal
    ├── api_server.bal
    └── data_processing.bal
```

### Data Requirements

- **Language**: Ballerina programming language code
- **Format**: Plain text `.bal` files
- **Quality**: Valid Ballerina syntax (highly recommended)
- **Size**: 100+ files for meaningful datasets (1000+ for best results)

## Dataset Curation

### Purpose

The DatasetCurator extracts and cleanses Ballerina code snippets from raw `.bal` files.

### Basic Usage

```python
from data_processing.curate_dataset import DatasetCurator

# Initialize curator
curator = DatasetCurator()

# Configure (optional)
curator.enable_train_val_test_split = True
curator.train_size = 0.8
curator.val_size = 0.1
curator.test_size = 0.1
curator.random_seed = 42

# Get user confirmation
if curator.get_user_confirmation():
    # Process datasets
    curator.process_bal_files()
```

### Configuration Options

```python
curator = DatasetCurator()

# Enable train/val/test splitting
curator.enable_train_val_test_split = True

# Set split ratios (must sum to 1.0)
curator.train_size = 0.8
curator.val_size = 0.1
curator.test_size = 0.1

# Reproducibility
curator.random_seed = 42

# Output paths
curator.repo_dir = "custom/path/to/bal/files"
curator.output_dir = "custom/output/path"
```

### Output Files

Curation generates timestamped output files:

```
data/raw/
├── dataset_2025-05-22_14-30-45.txt      # Combined dataset
├── train_2025-05-22_14-30-45.txt         # Training set (80%)
├── val_2025-05-22_14-30-45.txt           # Validation set (10%)
└── test_2025-05-22_14-30-45.txt          # Test set (10%)
```

### Script Usage

```bash
cd data-processing
python curate_dataset.py

# Follow prompts:
# Source directory: ../data-bal-files
# Output directory: ../data/raw
# train_val_test split: True
# Proceed? (y/n): y
```

## Dataset Formatting

### Purpose

The DatasetFormatter converts curated datasets into formats suitable for training.

### Basic Usage

```python
from data_processing.format_dataset import DatasetFormatter

# Initialize formatter
formatter = DatasetFormatter()

# Configure (optional)
formatter.enable_train_val_test_split = True

# Format datasets
formatter.process_all()
```

### Configuration Options

```python
formatter = DatasetFormatter(
    source_dir="../data/raw",           # Directory with curated datasets
    output_dir="../data/block-formatted", # Block format output
    chatml_dir="../data/chatML",         # ChatML format output
    enable_split=True                    # Enable train/val/test split
)
```

### Output Formats

#### 1. Block Format
```
<|start_of_block|>
function greet(string name) returns string {
    return "Hello, " + name;
}
<|end_of_block|>
```

#### 2. ChatML Format
```
<|im_start|>user
Complete this Ballerina function:
function add(int a, int b) returns
<|im_end|>
<|im_start|>assistant
function add(int a, int b) returns int {
    return a + b;
}
<|im_end|>
```

### Script Usage

```bash
cd data-processing
python format_dataset.py

# Follow prompts:
# Source directory: ../data/raw
# Output directory: ../data/block-formatted
# ChatML directory: ../data/chatML
# train_val_test split: True
# Proceed? (y/n): y
```

### Output Structure

```
data/
├── raw/
│   ├── dataset_*.txt
│   ├── train_*.txt
│   ├── val_*.txt
│   └── test_*.txt
├── block-formatted/
│   ├── dataset_*.txt
│   ├── train_*.txt
│   ├── val_*.txt
│   └── test_*.txt
└── chatML/
    ├── dataset_*.txt
    ├── train_*.txt
    ├── val_*.txt
    └── test_*.txt
```

## Supported Formats

### ChatML (Chat Markup Language)

**Structure**:
```
<|im_start|>role
content
<|im_end|>
```

**Example**:
```
<|im_start|>system
You are a helpful Ballerina code assistant.
<|im_end|>
<|im_start|>user
How do I define a service in Ballerina?
<|im_end|>
<|im_start|>assistant
In Ballerina, you define a service using:

service /api on new http:Listener(9090) {
    resource function get hello() returns string {
        return "Hello, World!";
    }
}
<|im_end|>
```

**Advantages**:
- Standard format for chat models
- Clear role separation
- Suitable for instruction-tuning

### Block Format

**Structure**:
```
<|start_of_block|>
code_content
<|end_of_block|>
```

**Example**:
```
<|start_of_block|>
import ballerina/http;

public function main() {
    var result = hello();
    io:println(result);
}

function hello() returns string {
    return "Hello, Ballerina!";
}
<|end_of_block|>
```

**Advantages**:
- Simple code block format
- Good for code completion
- Minimal overhead

## Advanced Usage

### Custom Data Processing

```python
from data_processing.format_dataset import DatasetFormatter
from data_processing.curate_dataset import DatasetCurator

# Step 1: Curation with custom settings
curator = DatasetCurator()
curator.repo_dir = "custom/bal/files"
curator.output_dir = "custom/output"
curator.train_size = 0.9
curator.val_size = 0.05
curator.test_size = 0.05
curator.process_bal_files()

# Step 2: Formatting with custom settings
formatter = DatasetFormatter(
    source_dir=curator.output_dir,
    output_dir="custom/formatted",
    enable_split=True
)
formatter.process_all()
```

### Filtering by File Size

```python
from data_processing.curate_dataset import DatasetCurator
import os

curator = DatasetCurator()

# Custom filtering
min_size = 100  # bytes
max_size = 50000  # bytes

files = []
for f in os.listdir(curator.repo_dir):
    path = os.path.join(curator.repo_dir, f)
    if min_size <= os.path.getsize(path) <= max_size:
        files.append(path)
```

### Memory-Efficient Processing

For large datasets, process in chunks:

```python
from data_processing.format_dataset import DatasetFormatter
import os

formatter = DatasetFormatter()

# Process files one at a time
for file in os.listdir(formatter.source_dir):
    if file.endswith('.txt'):
        # Process individually
        formatter.process_file(os.path.join(formatter.source_dir, file))
```

## Quality Assurance

### Dataset Validation

```python
import os
import json

def validate_dataset(dataset_path):
    """Validate formatted dataset"""
    errors = []
    
    with open(dataset_path, 'r') as f:
        content = f.read()
    
    # Check for proper formatting
    if '<|im_start|>' in content:
        start_count = content.count('<|im_start|>')
        end_count = content.count('<|im_end|>')
        if start_count != end_count:
            errors.append(f"Mismatched tags: {start_count} starts, {end_count} ends")
    
    # Check file size
    file_size = len(content)
    if file_size < 1000:
        errors.append(f"Dataset too small: {file_size} bytes")
    
    return errors

# Validate
errors = validate_dataset("data/chatML/train_*.txt")
if errors:
    print("Validation errors:", errors)
else:
    print("Dataset is valid!")
```

### Statistics

```python
import os

def get_dataset_stats(dataset_path):
    """Get dataset statistics"""
    with open(dataset_path, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    words = content.split()
    
    return {
        'lines': len(lines),
        'words': len(words),
        'chars': len(content),
        'avg_line_length': len(content) / len(lines) if lines else 0
    }

stats = get_dataset_stats("data/chatML/train_*.txt")
print(f"Lines: {stats['lines']}")
print(f"Words: {stats['words']}")
print(f"Characters: {stats['chars']}")
```

## Troubleshooting

### Issue: "Directory does not exist"

**Solution**:
```bash
# Verify directory structure
ls -la data-bal-files/
# Create if missing
mkdir -p data-bal-files
```

### Issue: "No .bal files found"

**Solution**:
```bash
# Check file extensions
find data-bal-files -name "*.bal"

# Rename if needed
rename 's/\.txt$/.bal/' data-bal-files/*
```

### Issue: "Dataset is empty"

**Solution**:
1. Verify source directory has files
2. Check file permissions: `chmod 644 data-bal-files/*`
3. Ensure valid Ballerina code in files

### Issue: "Out of memory during formatting"

**Solution**:
```python
# Process in smaller batches
formatter = DatasetFormatter()

# Set chunk size
batch_size = 10000  # lines
chunks = []
with open(formatter.source_dir + "/dataset.txt") as f:
    chunk = []
    for i, line in enumerate(f):
        chunk.append(line)
        if i % batch_size == 0:
            chunks.append(''.join(chunk))
            chunk = []
```

### Issue: "Mismatched ChatML tags"

**Solution**:
```python
# Auto-fix mismatched tags
def fix_chatml_tags(content):
    # Count and fix mismatches
    while content.count('<|im_start|>') != content.count('<|im_end|>'):
        if content.count('<|im_start|>') > content.count('<|im_end|>'):
            content += '<|im_end|>'
        else:
            # Remove extra end tags
            content = content.replace('<|im_end|>', '', 1)
    return content
```

## Best Practices

1. **Use Train/Val/Test Splits**: Always enable splitting for proper evaluation
2. **Set Random Seed**: Use `random_seed=42` for reproducibility
3. **Validate Formats**: Always validate output before training
4. **Track Versions**: Use timestamps and version control
5. **Backup Original Data**: Keep raw data in version control
6. **Monitor Sizes**: Ensure splits are balanced (not too skewed)
7. **Document Changes**: Note any preprocessing applied

## Performance Tips

- **Fast Processing**: Use SSD for file I/O
- **Parallel Processing**: Process multiple files simultaneously
- **Memory Efficient**: Stream large files instead of loading entirely
- **Format Choice**: Use ChatML for chat models, Block for completion models

---

For training procedures, see [TRAINING.md](TRAINING.md).
For deployment, see [INFERENCE.md](INFERENCE.md).
