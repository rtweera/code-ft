# Project Architecture

Comprehensive overview of the project structure, components, and data flow.

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [Component Overview](#component-overview)
3. [Data Flow](#data-flow)
4. [Key Classes and Modules](#key-classes-and-modules)
5. [Dependencies](#dependencies)

## Directory Structure

```
code-ft/
├── data-processing/                    # Data preparation pipeline
│   ├── __pycache__/
│   ├── curate_dataset.py              # Extract Ballerina code from .bal files
│   ├── format_dataset.py              # Format datasets into training formats
│   ├── regex_patterns.py              # Regex patterns for code parsing
│   └── utils.py                       # Helper utilities
│
├── training/                           # Training implementations
│   ├── SFT/                           # Supervised Fine-Tuning
│   │   ├── Kagggle/                   # Training with Kaggle datasets
│   │   │   └── [Training scripts]
│   │   └── Tweets/                    # Training with tweet datasets
│   │       ├── REPORTS.md             # Training reports and metrics
│   │       └── [Training scripts]
│   │
│   └── LoRA/                          # Low-Rank Adaptation
│       └── [LoRA training scripts]
│
├── models/                             # Model utilities
│   └── README.md                       # Model building and deployment guide
│
├── utils/                              # Utility functions
│   ├── fine_tuning_profiler.py        # Resource monitoring (GPU, CPU, memory)
│   └── matrix_difference.py           # Matrix utilities for model analysis
│
├── neural-networks/                    # Neural network components
│   └── [Educational materials]
│
├── math/                               # Mathematical documentation
│   └── formular.md                    # Mathematical formulas and equations
│
├── explanations/                       # Educational explanations
│   └── layer_normalization_intuition.md # Deep dive into layer normalization
│
├── concepts-examples/                  # Practical concept examples
│   └── [Example implementations]
│
├── docs/                               # Comprehensive documentation
│   ├── SETUP.md                       # Installation and setup guide
│   ├── ARCHITECTURE.md                # This file
│   ├── DATA_PROCESSING.md             # Data pipeline documentation
│   ├── TRAINING.md                    # Training procedures
│   ├── INFERENCE.md                   # Model deployment and inference
│   ├── API_REFERENCE.md               # API documentation
│   ├── CONTRIBUTING.md                # Contribution guidelines
│   ├── FAQ.md                         # Frequently asked questions
│   ├── HUGGINGFACE-TO-OLLAMA.md       # Export to Ollama guide
│   └── METADATA.md                    # Metadata documentation
│
├── archive/                            # Archived/deprecated code
│
├── .git/                               # Git repository
├── .gitignore                          # Git ignore rules
├── LICENSE                             # Apache License 2.0
├── README.md                           # Project README
└── requirements.txt                    # Python dependencies

```

## Component Overview

### Data Processing Pipeline

The data processing pipeline consists of three main stages:

```
Raw .bal Files
    ↓
[DatasetCurator]
    ↓
Raw Dataset (txt files)
    ↓
[DatasetFormatter]
    ↓
Block Format + ChatML Format
    ↓
Training Ready Datasets
```

#### Components:

1. **DatasetCurator** (`data-processing/curate_dataset.py`)
   - **Purpose**: Extract Ballerina code snippets from `.bal` source files
   - **Input**: Directory of `.bal` files
   - **Output**: Curated dataset text files
   - **Features**:
     - Automatic train/validation/test splitting
     - Date-timestamped output files
     - Configurable split ratios

2. **DatasetFormatter** (`data-processing/format_dataset.py`)
   - **Purpose**: Convert curated datasets into training-ready formats
   - **Input**: Curated dataset text files
   - **Output**: ChatML-formatted and block-formatted datasets
   - **Features**:
     - Multiple format support (ChatML, block)
     - Optional train/val/test splitting
     - Batch processing

3. **Regex Patterns** (`data-processing/regex_patterns.py`)
   - **Purpose**: Define parsing patterns for Ballerina code
   - **Contains**: Regular expressions for code extraction and validation

4. **Utilities** (`data-processing/utils.py`)
   - **Purpose**: Helper functions for data processing
   - **Functions**: File management, data validation, etc.

### Training Pipeline

The project supports two training approaches:

#### 1. Supervised Fine-Tuning (SFT)
- **Location**: `training/SFT/`
- **Datasets**: Kaggle and Twitter-based data
- **Approach**: Full model fine-tuning
- **Use Cases**: 
  - Maximum performance
  - Full model adaptation
  - Higher computational requirements

#### 2. Low-Rank Adaptation (LoRA)
- **Location**: `training/LoRA/`
- **Approach**: Parameter-efficient fine-tuning
- **Benefits**:
  - Lower GPU memory requirements
  - Faster training
  - Smaller model files
  - Easy adapter merging

### Model Utilities

**Module**: `models/`

Provides utilities for:
- Merging LoRA adapters with base models
- Converting models to GGUF format
- Model export and deployment
- Weight optimization

See `models/README.md` for detailed procedures.

### Monitoring and Profiling

**Module**: `utils/fine_tuning_profiler.py`

**ResourceMonitor Class**:
- Tracks GPU usage (memory, utilization)
- Monitors system resources (CPU, RAM)
- Logs performance metrics over time
- Supports persistent logging to CSV
- Provides visualization capabilities

**Features**:
```python
# Initialize monitor
monitor = ResourceMonitor(interval=5, log_path="training_log.csv")

# Start monitoring
monitor.start()

# During training...

# Stop monitoring
monitor.stop()

# Access metrics
metrics = monitor.get_resource_log()
```

## Data Flow

### Complete Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA PROCESSING PHASE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Raw Ballerina Files → Curation → Formatting → Training Data   │
│                                                                 │
│  [curate_dataset.py]  [format_dataset.py]                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    TRAINING PHASE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐         ┌──────────────────┐              │
│  │  SFT Training   │         │  LoRA Training   │              │
│  │                 │         │                  │              │
│  │ • Full tuning   │         │ • Parameter eff. │              │
│  │ • Higher perf   │         │ • Lower mem      │              │
│  │ • Slower        │         │ • Faster         │              │
│  └─────────────────┘         └──────────────────┘              │
│                              ↓                                 │
│                    [ResourceMonitor tracks metrics]            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    MODEL EXPORT PHASE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Fine-tuned Model → Merge (if LoRA) → GGUF Format → Ollama    │
│                                                                 │
│                     [models/ utilities]                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT PHASE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Ollama/vLLM Deployment → API Endpoint → Client Applications   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Key Classes and Modules

### DatasetCurator

```python
class DatasetCurator:
    """Extracts Ballerina code from .bal files."""
    
    def __init__(self)
    def get_user_confirmation(self) -> bool
    def validate_split_ratios(self) -> None
    def process_bal_files(self) -> None
    def extract_code(self, file_path: str) -> List[str]
    def save_dataset(self) -> None
```

**Usage**:
```python
curator = DatasetCurator()
curator.enable_train_val_test_split = True
curator.train_size = 0.8
curator.process_bal_files()
```

### DatasetFormatter

```python
class DatasetFormatter:
    """Formats curated datasets for training."""
    
    def __init__(self, source_dir=None, output_dir=None, chatml_dir=None)
    def setup_directories(self) -> None
    def format_to_chatml(self) -> None
    def format_to_blocks(self) -> None
    def process_all(self) -> None
```

**Usage**:
```python
formatter = DatasetFormatter()
formatter.process_all()
```

### ResourceMonitor

```python
class ResourceMonitor:
    """Monitors GPU and system resources during training."""
    
    def __init__(self, interval=5, log_path=None, verbose=False)
    def start(self) -> None
    def stop(self) -> None
    def get_resource_log(self) -> pd.DataFrame
    def save_log(self, path: str) -> None
    def load_log(self, path: str) -> None
    def get_summary(self) -> Dict
    def plot_metrics(self) -> None
```

**Usage**:
```python
monitor = ResourceMonitor(interval=5, log_path="training_metrics.csv")
monitor.start()
# ... training code ...
monitor.stop()
monitor.plot_metrics()
```

## Dependencies

### Core Dependencies

```
torch >= 2.0.0              # Deep learning framework
transformers >= 4.30.0      # Model architectures and utilities
peft >= 0.4.0               # Parameter-efficient fine-tuning
datasets >= 2.10.0          # Dataset loading and processing
accelerate >= 0.20.0        # Distributed training
bitsandbytes >= 0.40.0      # 8-bit optimization
```

### Data Processing Dependencies

```
pandas >= 2.0.0             # Data manipulation
numpy >= 2.0.0              # Numerical computing
regex >= 2023.0.0           # Advanced regex patterns
```

### Monitoring and Visualization

```
psutil >= 5.9.0             # System resource monitoring
pynvml >= 12.0.0            # NVIDIA GPU monitoring
matplotlib >= 3.5.0         # Plotting and visualization
```

### Deployment Dependencies

```
python-dateutil >= 2.8.0    # Date utilities
pytz >= 2023.0              # Timezone handling
```

## Architecture Patterns

### Factory Pattern
Used in dataset creation for different formats (ChatML, Block).

### Observer Pattern
ResourceMonitor observes system metrics at intervals.

### Pipeline Pattern
Data flows through: Raw → Curated → Formatted → Training → Export → Deploy

### Strategy Pattern
Different training strategies (SFT, LoRA) with common interface.

## Configuration Management

Configuration is handled through:

1. **Constructor Parameters**: Direct instantiation
   ```python
   formatter = DatasetFormatter(
       source_dir="custom/path",
       output_dir="output/path",
       enable_split=True
   )
   ```

2. **Class Attributes**: Post-instantiation modification
   ```python
   curator = DatasetCurator()
   curator.enable_train_val_test_split = True
   curator.train_size = 0.8
   ```

3. **Environment Variables**: System-level configuration (used in deployment)

## Performance Considerations

### Memory Optimization
- LoRA for parameter-efficient training
- Gradient checkpointing to reduce activation memory
- Mixed precision training (fp16) to reduce memory usage

### Computation Optimization
- Distributed training using `accelerate`
- Batch processing in data pipeline
- GPU acceleration for training and inference

### I/O Optimization
- Asynchronous data loading
- Prefetching during training
- Efficient file format usage (GGUF for deployment)

---

For detailed information about specific components, see:
- [DATA_PROCESSING.md](DATA_PROCESSING.md) for data pipeline
- [TRAINING.md](TRAINING.md) for training procedures
- [INFERENCE.md](INFERENCE.md) for deployment
