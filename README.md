# code-ft: Fine-Tuning Small Language Models for Ballerina Code Completion

A comprehensive framework for fine-tuning Small Language Models (SLMs) to generate and complete Ballerina programming language code. This project leverages modern techniques like LoRA (Low-Rank Adaptation) and Supervised Fine-Tuning (SFT) to create efficient, specialized code completion models.

## 🎯 Project Goals

- **Develop specialized code completion models** for Ballerina programming language
- **Optimize inference efficiency** using small language models instead of large ones
- **Provide end-to-end pipeline** from raw code datasets to deployable models
- **Support multiple training approaches** (SFT and LoRA) for flexibility
- **Enable easy deployment** with Ollama and other inference frameworks

## ✨ Key Features

- **Dataset Curation**: Extract and process Ballerina code from raw `.bal` files
- **Data Formatting**: Convert datasets into ChatML and block formats for training
- **Flexible Training**: Support for both SFT and LoRA fine-tuning approaches
- **Resource Monitoring**: Track GPU and system resource usage during training
- **Model Export**: Convert fine-tuned models to Ollama-compatible GGUF format
- **Comprehensive Utilities**: Helper tools for data processing, profiling, and model optimization

## 📁 Project Structure

```
code-ft/
├── data-processing/          # Dataset curation and formatting
│   ├── curate_dataset.py     # Extract Ballerina code from .bal files
│   ├── format_dataset.py     # Format datasets for training
│   └── regex_patterns.py     # Pattern definitions for parsing
├── training/                 # Training implementations
│   ├── SFT/                  # Supervised Fine-Tuning
│   │   ├── Kagggle/
│   │   └── Tweets/
│   └── LoRA/                 # Low-Rank Adaptation
├── models/                   # Model utilities and merging
├── utils/                    # Utility functions
│   ├── fine_tuning_profiler.py  # Resource monitoring
│   └── matrix_difference.py     # Matrix utilities
├── neural-networks/          # Neural network components
├── math/                     # Mathematical formulas and concepts
├── explanations/             # Educational materials and intuitions
└── docs/                     # Detailed documentation

```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- CUDA-compatible GPU (recommended)
- 16GB+ RAM (8GB minimum)

### Installation

```bash
# Clone the repository
git clone https://github.com/rtweera/code-ft.git
cd code-ft

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Workflow

1. **Prepare Data**
   ```bash
   cd data-processing
   python curate_dataset.py  # Extract Ballerina code
   python format_dataset.py  # Format for training
   ```

2. **Train Model**
   ```bash
   cd training/SFT  # or training/LoRA
   # Run training scripts (details in TRAINING.md)
   ```

3. **Deploy Model**
   ```bash
   # See INFERENCE.md for deployment instructions
   ```

## 📚 Documentation

- **[SETUP.md](docs/SETUP.md)** - Detailed setup and installation guide
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Project structure and component overview
- **[DATA_PROCESSING.md](docs/DATA_PROCESSING.md)** - Data pipeline documentation
- **[TRAINING.md](docs/TRAINING.md)** - Training procedures and best practices
- **[INFERENCE.md](docs/INFERENCE.md)** - Model deployment and inference
- **[API_REFERENCE.md](docs/API_REFERENCE.md)** - Module and class documentation
- **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** - Contribution guidelines
- **[FAQ.md](docs/FAQ.md)** - Frequently asked questions

## 🔧 Key Components

### Data Processing
- **DatasetCurator**: Extracts code from `.bal` files with train/val/test splitting
- **DatasetFormatter**: Converts curated datasets into ChatML and block formats

### Training
- **SFT (Supervised Fine-Tuning)**: Standard fine-tuning approach
- **LoRA (Low-Rank Adaptation)**: Parameter-efficient fine-tuning

### Utilities
- **ResourceMonitor**: Tracks GPU and system resources during training
- **Matrix Utilities**: Helper functions for model optimization

## 🛠️ System Requirements

### Minimum
- CPU: 4-core processor
- RAM: 8GB
- Storage: 50GB (for datasets and models)

### Recommended
- CPU: 8+ cores
- RAM: 16GB+
- GPU: NVIDIA GPU with 6GB+ VRAM
- Storage: 100GB+ (for multiple model versions)

## 🔗 Related Technologies

- **Base Models**: Qwen, Mistral, CodeLLaMA (customizable)
- **Frameworks**: Hugging Face Transformers, PyTorch, PEFT
- **Deployment**: Ollama, vLLM, TensorRT
- **Languages**: Ballerina programming language

## 📋 License

This project is licensed under the [Apache License 2.0](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 💬 Getting Help

- Check [FAQ.md](docs/FAQ.md) for common issues
- Review existing documentation in the `docs/` directory
- Open an issue on GitHub for bugs and feature requests

## 📝 Citation

If you use this project in your research or work, please cite:

```bibtex
@software{code_ft,
  title={code-ft: Fine-Tuning Small Language Models for Ballerina Code Completion},
  author={rtweera},
  year={2025},
  url={https://github.com/rtweera/code-ft}
}
```

## 🎓 Educational Resources

This project includes educational materials:
- **Math Formulas**: Neural network memory calculations and optimization formulas
- **Explanations**: In-depth intuitions about layer normalization and neural network concepts
- **Concept Examples**: Practical examples of key machine learning concepts

---

**Last Updated**: 2025-05-22 
