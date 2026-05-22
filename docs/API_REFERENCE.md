# API Reference

Detailed API documentation for key modules and classes.

## Table of Contents

1. [DatasetCurator](#datasetcurator)
2. [DatasetFormatter](#datasetformatter)
3. [ResourceMonitor](#resourcemonitor)
4. [Utility Functions](#utility-functions)

## DatasetCurator

**Module**: `data-processing/curate_dataset.py`

Extracts and processes Ballerina code from `.bal` files.

### Class: DatasetCurator

```python
class DatasetCurator:
    """Class to handle the curation of raw dataset files from bal files."""
```

#### Constructor

```python
def __init__(self):
    """Initialize paths, filenames, and configuration."""
```

**Attributes**:
- `script_dir` (str): Directory of the script
- `repo_dir` (str): Path to directory with `.bal` files
- `output_dir` (str): Output directory for curated datasets
- `enable_train_val_test_split` (bool): Enable train/val/test splitting (default: False)
- `train_size` (float): Proportion for training (default: 0.8)
- `val_size` (float): Proportion for validation (default: 0.1)
- `test_size` (float): Proportion for testing (default: 0.1)
- `random_seed` (int): Seed for reproducibility (default: 42)

#### Methods

##### get_user_confirmation()

```python
def get_user_confirmation(self) -> bool:
    """Get confirmation from user before proceeding."""
```

**Returns**: `bool` - True if user confirms, False otherwise

**Example**:
```python
curator = DatasetCurator()
if curator.get_user_confirmation():
    curator.process_bal_files()
```

##### validate_split_ratios()

```python
def validate_split_ratios(self) -> None:
    """Validate that split ratios are valid."""
```

**Raises**: `ValueError` if ratios invalid

**Example**:
```python
curator.train_size = 0.8
curator.val_size = 0.1
curator.test_size = 0.1
curator.validate_split_ratios()  # OK
```

##### process_bal_files()

```python
def process_bal_files(self) -> None:
    """Extract and process Ballerina code from .bal files."""
```

**Behavior**:
- Reads all `.bal` files from `repo_dir`
- Extracts code snippets
- Creates dataset files with timestamps
- Optionally splits into train/val/test

**Example**:
```python
curator = DatasetCurator()
curator.repo_dir = "path/to/bal/files"
curator.output_dir = "path/to/output"
curator.process_bal_files()
```

##### extract_code()

```python
def extract_code(self, file_path: str) -> List[str]:
    """Extract code snippets from a .bal file."""
```

**Parameters**:
- `file_path` (str): Path to `.bal` file

**Returns**: `List[str]` - List of extracted code snippets

**Example**:
```python
snippets = curator.extract_code("module/main.bal")
print(f"Extracted {len(snippets)} snippets")
```

##### save_dataset()

```python
def save_dataset(self) -> None:
    """Save processed dataset to output files."""
```

**Creates**:
- `dataset_TIMESTAMP.txt` - Combined dataset
- `train_TIMESTAMP.txt` - Training set (if split enabled)
- `val_TIMESTAMP.txt` - Validation set (if split enabled)
- `test_TIMESTAMP.txt` - Test set (if split enabled)

---

## DatasetFormatter

**Module**: `data-processing/format_dataset.py`

Formats curated datasets into training-ready formats.

### Class: DatasetFormatter

```python
class DatasetFormatter:
    """Class for formatting curated code datasets."""
```

#### Constructor

```python
def __init__(self, source_dir=None, output_dir=None, chatml_dir=None, enable_split=False):
    """Initialize the DatasetFormatter with directory paths."""
```

**Parameters**:
- `source_dir` (str, optional): Directory with curated datasets
- `output_dir` (str, optional): Output directory for block format
- `chatml_dir` (str, optional): Output directory for ChatML format
- `enable_split` (bool): Enable train/val/test splitting (default: False)

**Attributes**:
- `source_dir` (str): Path to source datasets
- `output_dir` (str): Path for block-formatted output
- `chatml_dir` (str): Path for ChatML-formatted output
- `enable_train_val_test_split` (bool): Split configuration

#### Methods

##### prompt_confirmation()

```python
def prompt_confirmation(self) -> bool:
    """Ask for user confirmation before proceeding."""
```

**Returns**: `bool` - True if user confirms

##### setup_directories()

```python
def setup_directories(self) -> None:
    """Check and create necessary directories."""
```

**Raises**:
- `FileNotFoundError` if source directory doesn't exist
- `ValueError` if source directory is empty

##### format_to_chatml()

```python
def format_to_chatml(self) -> None:
    """Convert dataset to ChatML format."""
```

**Behavior**:
- Reads raw dataset files
- Formats to ChatML conversation format
- Saves to `chatml_dir`

**Output Format**:
```
<|im_start|>user
Complete this function:
function add(int a, int b) returns
<|im_end|>
<|im_start|>assistant
function add(int a, int b) returns int {
    return a + b;
}
<|im_end|>
```

##### format_to_blocks()

```python
def format_to_blocks(self) -> None:
    """Convert dataset to block format."""
```

**Behavior**:
- Reads raw dataset files
- Wraps in block markers
- Saves to `output_dir`

**Output Format**:
```
<|start_of_block|>
code snippet here
<|end_of_block|>
```

##### process_all()

```python
def process_all(self) -> None:
    """Process all datasets in all formats."""
```

**Equivalent to**:
```python
formatter.setup_directories()
formatter.format_to_chatml()
formatter.format_to_blocks()
```

**Example**:
```python
formatter = DatasetFormatter()
formatter.process_all()
```

---

## ResourceMonitor

**Module**: `utils/fine_tuning_profiler.py`

Monitors GPU and system resources during training.

### Class: ResourceMonitor

```python
class ResourceMonitor:
    """Monitor GPU and system resources during training."""
```

#### Constructor

```python
def __init__(self, interval=5, log_path=None, verbose=False):
    """Initialize the ResourceMonitor."""
```

**Parameters**:
- `interval` (int): Seconds between resource checks (default: 5)
- `log_path` (str, optional): Path to CSV file for logging
- `verbose` (bool): Print to console (default: False)

**Attributes**:
- `interval` (int): Monitoring interval
- `log_path` (str): Path to persistent log
- `verbose` (bool): Verbosity flag
- `resource_log` (list): In-memory resource history
- `event_log` (list): In-memory event history

#### Methods

##### start()

```python
def start(self) -> None:
    """Start resource monitoring."""
```

**Behavior**: Begins background thread for monitoring

**Example**:
```python
monitor = ResourceMonitor()
monitor.start()
```

##### stop()

```python
def stop(self) -> None:
    """Stop resource monitoring."""
```

**Behavior**: Ends background thread

**Example**:
```python
monitor.stop()
```

##### get_resource_log()

```python
def get_resource_log(self) -> pd.DataFrame:
    """Get resource usage history as DataFrame."""
```

**Returns**: `pd.DataFrame` with columns:
- `timestamp`: When measurement was taken
- `gpu_memory_used`: GPU memory in MB
- `gpu_utilization`: GPU utilization percent
- `cpu_usage`: CPU utilization percent
- `cpu_memory`: System RAM usage in MB

**Example**:
```python
monitor = ResourceMonitor()
monitor.start()
# ... training ...
monitor.stop()

df = monitor.get_resource_log()
print(df.describe())
```

##### get_event_log()

```python
def get_event_log(self) -> List[Dict]:
    """Get event log."""
```

**Returns**: `List[Dict]` with event records

##### save_log()

```python
def save_log(self, path: str = None) -> None:
    """Save log to CSV file."""
```

**Parameters**:
- `path` (str): Path to save CSV (uses log_path if not provided)

**Example**:
```python
monitor.save_log("training_metrics.csv")
```

##### load_log()

```python
def load_log(self, path: str = None, silent: bool = False) -> None:
    """Load log from CSV file."""
```

**Parameters**:
- `path` (str): Path to CSV (uses log_path if not provided)
- `silent` (bool): Suppress output

##### get_summary()

```python
def get_summary(self) -> Dict:
    """Get summary statistics."""
```

**Returns**: `Dict` with:
- `max_gpu_memory`: Maximum GPU memory used
- `avg_gpu_utilization`: Average GPU utilization
- `max_cpu_usage`: Peak CPU usage
- `avg_cpu_memory`: Average system RAM usage
- `total_events`: Number of events logged

**Example**:
```python
summary = monitor.get_summary()
print(f"Peak GPU Memory: {summary['max_gpu_memory']} MB")
```

##### plot_metrics()

```python
def plot_metrics(self, save_path: str = None) -> None:
    """Plot resource usage metrics."""
```

**Parameters**:
- `save_path` (str, optional): Path to save plot image

**Generates**: Visualization of resource usage over time

**Example**:
```python
monitor.plot_metrics("training_plot.png")
```

---

## Utility Functions

### data_processing/utils.py

#### get_most_recent_file_with_prefix()

```python
def get_most_recent_file_with_prefix(directory: str, prefix: str) -> str:
    """Get the most recently modified file with given prefix."""
```

**Parameters**:
- `directory` (str): Directory to search
- `prefix` (str): File prefix to match

**Returns**: `str` - Path to most recent matching file

**Example**:
```python
from data_processing.utils import get_most_recent_file_with_prefix

latest_dataset = get_most_recent_file_with_prefix(
    "data/raw",
    "dataset_"
)
print(latest_dataset)  # "data/raw/dataset_2025-05-22_14-30-45.txt"
```

### utils/matrix_difference.py

#### Matrix Comparison Functions

```python
def matrix_difference(matrix1: np.ndarray, matrix2: np.ndarray) -> Dict:
    """Compare two matrices and return statistics."""
```

**Parameters**:
- `matrix1` (np.ndarray): First matrix
- `matrix2` (np.ndarray): Second matrix

**Returns**: `Dict` with:
- `mean_diff`: Mean absolute difference
- `max_diff`: Maximum absolute difference
- `correlation`: Correlation coefficient

**Example**:
```python
from utils.matrix_difference import matrix_difference

diff = matrix_difference(weight_before, weight_after)
print(f"Mean weight change: {diff['mean_diff']}")
```

---

## Type Hints

Common type hints used in the codebase:

```python
from typing import List, Dict, Tuple, Optional, Union
import pandas as pd
import numpy as np

# Dataset paths
dataset_path: str

# Configuration
enable_split: bool
train_size: float  # 0.0-1.0

# Data structures
resource_log: pd.DataFrame
event_log: List[Dict]

# Arrays
matrix: np.ndarray
embeddings: np.ndarray
```

---

## Error Handling

### Common Exceptions

```python
# File not found
FileNotFoundError("Dataset directory not found")

# Invalid configuration
ValueError("Split ratios must sum to 1.0")

# CUDA errors
RuntimeError("CUDA out of memory")

# Tokenization errors
ValueError("Tokenization failed")
```

### Handling Errors

```python
from data_processing.curate_dataset import DatasetCurator

try:
    curator = DatasetCurator()
    curator.validate_split_ratios()
except ValueError as e:
    print(f"Configuration error: {e}")
```

---

For usage examples, see individual documentation files:
- [DATA_PROCESSING.md](DATA_PROCESSING.md)
- [TRAINING.md](TRAINING.md)
- [INFERENCE.md](INFERENCE.md)
