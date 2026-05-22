# Frequently Asked Questions (FAQ)

Common questions and answers about the code-ft project.

## Table of Contents

1. [General Questions](#general-questions)
2. [Setup and Installation](#setup-and-installation)
3. [Data Processing](#data-processing)
4. [Training](#training)
5. [Inference and Deployment](#inference-and-deployment)
6. [Troubleshooting](#troubleshooting)
7. [Performance and Optimization](#performance-and-optimization)

## General Questions

### What is code-ft?

**Answer**: code-ft is a framework for fine-tuning Small Language Models (SLMs) to generate and complete Ballerina programming language code. It provides end-to-end tools from data preparation to model deployment.

### Why use SLMs instead of larger models?

**Answer**: SLMs offer:
- Lower computational requirements
- Faster inference
- Easier deployment on resource-constrained devices
- Competitive performance with proper fine-tuning
- Better suited for specific domains like code generation

### What programming language is code-ft written in?

**Answer**: Python 3.10+. Python is widely used in ML/AI projects and offers excellent libraries for deep learning.

### Do I need a GPU to use code-ft?

**Answer**: While a GPU significantly speeds up training, it's not strictly necessary. You can:
- Train on CPU (much slower, good for prototyping)
- Use cloud GPUs (AWS, Google Cloud, etc.)
- Use other platforms' free GPU access (Google Colab, Kaggle)

### What license is this project under?

**Answer**: Apache License 2.0. See [LICENSE](../LICENSE) for details.

### How can I contribute?

**Answer**: See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Setup and Installation

### I'm getting "Python not found" error

**Answer**:
1. Verify Python installation: `python --version`
2. Ensure Python is in PATH
3. Try `python3` instead of `python`
4. Download Python from [python.org](https://python.org)

### How do I create a virtual environment?

**Answer**:
```bash
# Create
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

See [SETUP.md](SETUP.md) for detailed instructions.

### I'm getting "pip: command not found"

**Answer**:
```bash
# Use Python module
python -m pip --version

# Upgrade
python -m pip install --upgrade pip

# Install packages
python -m pip install -r requirements.txt
```

### CUDA is not being recognized

**Answer**:
1. Verify installation: `nvidia-smi`
2. Check CUDA path is in PATH environment variable
3. Reinstall CUDA toolkit
4. See [SETUP.md - GPU Setup](SETUP.md#gpu-setup) for detailed steps

### How do I know if my GPU is detected?

**Answer**:
```python
import torch
print(f"GPU Available: {torch.cuda.is_available()}")
print(f"GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
print(f"CUDA Version: {torch.version.cuda}")
```

## Data Processing

### What format should my code files be in?

**Answer**: `.bal` (Ballerina) files organized in directories. See [DATA_PROCESSING.md - Data Sources](DATA_PROCESSING.md#data-sources).

### How many files do I need for a good dataset?

**Answer**: 
- Minimum: 100+ files
- Good: 500-1000 files
- Excellent: 2000+ files
- More data generally improves results, but quality matters too

### What if my .bal files have syntax errors?

**Answer**:
- The curator will extract code anyway
- Formatter may produce inconsistent results
- Best practice: Clean your data before processing
- Consider adding validation step

### How do I know if my dataset is good?

**Answer**: 
1. Check dataset statistics:
   ```python
   import os
   file_size = os.path.getsize("dataset.txt")
   with open("dataset.txt") as f:
       lines = len(f.readlines())
   print(f"Size: {file_size} bytes, Lines: {lines}")
   ```

2. Sample and review the data
3. Check format is correct
4. Verify train/val/test split is balanced

### Can I use multiple datasets?

**Answer**: Yes!
```python
# Combine before formatting
with open("combined.txt", "w") as out:
    for dataset_file in ["dataset1.txt", "dataset2.txt"]:
        with open(dataset_file) as f:
            out.write(f.read() + "\n")
```

### What's the difference between ChatML and Block formats?

**Answer**:
- **ChatML**: Conversation format, good for instruction-tuning
- **Block**: Simple code blocks, good for completion tasks

See [DATA_PROCESSING.md - Supported Formats](DATA_PROCESSING.md#supported-formats).

## Training

### How do I choose between SFT and LoRA?

**Answer**: 
- **SFT**: Use if you have GPU memory (12GB+) and want best performance
- **LoRA**: Use if memory is limited (6GB) or you want faster training

See [TRAINING.md - Training Approaches](TRAINING.md#training-approaches).

### What hyperparameters should I use?

**Answer**: Start with defaults:
```python
learning_rate = 2e-4  # SFT or 5e-4 for LoRA
num_train_epochs = 3
batch_size = 4  # SFT or 8 for LoRA
warmup_steps = 500
```

Adjust based on training curves. See [TRAINING.md - Hyperparameters](TRAINING.md#hyperparameters).

### My training is very slow

**Answer**:
1. Check GPU usage: `nvidia-smi`
2. Increase batch size if possible
3. Enable mixed precision: `fp16=True`
4. Use LoRA instead of SFT
5. Reduce sequence length

### Training loss is not decreasing

**Answer**:
1. Check data loading
2. Lower learning rate
3. Verify model loads correctly
4. Check for NaN values
5. Try smaller batch size

### How long does training take?

**Answer**: Varies by:
- Model size (1.5B ~1-6 hours for SFT, 30 mins-2 hours for LoRA)
- Dataset size
- GPU type
- Hyperparameters

See [TRAINING.md - Performance Benchmarks](TRAINING.md#performance-benchmarks).

### How do I monitor training progress?

**Answer**:
```python
# Use ResourceMonitor
from utils.fine_tuning_profiler import ResourceMonitor

monitor = ResourceMonitor(log_path="metrics.csv")
monitor.start()
# ... training ...
monitor.stop()
monitor.plot_metrics()
```

See [TRAINING.md - Monitoring Training](TRAINING.md#monitoring-training).

## Inference and Deployment

### Can I use my SFT model directly for inference?

**Answer**: Yes!
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("./my_model")
tokenizer = AutoTokenizer.from_pretrained("./my_model")
# ... inference code ...
```

See [INFERENCE.md - Local Inference](INFERENCE.md#local-inference).

### How do I use a LoRA model for inference?

**Answer**: You need to either:
1. Merge before inference:
   ```python
   model = model.merge_and_unload()
   ```

2. Load with PEFT:
   ```python
   from peft import PeftModel
   model = PeftModel.from_pretrained(model, "adapter_path")
   ```

See [INFERENCE.md - With LoRA Adapter](INFERENCE.md#with-lora-adapter).

### What's the easiest way to deploy locally?

**Answer**: Use Ollama:
1. Convert model to GGUF
2. Create Modelfile
3. Run `ollama create model -f Modelfile`
4. Run `ollama run model`

See [INFERENCE.md - Ollama Deployment](INFERENCE.md#ollama-deployment).

### How do I deploy for production?

**Answer**:
1. Quantize model (reduce size)
2. Set up vLLM or similar server
3. Add authentication/rate limiting
4. Deploy on cloud platform
5. Monitor and log usage

See [INFERENCE.md - API Deployment](INFERENCE.md#api-deployment).

### What's the difference between GGUF and SafeTensors?

**Answer**:
- **SafeTensors**: PyTorch format, good for research/fine-tuning
- **GGUF**: Optimized for inference with quantization support

### Can I quantize my model?

**Answer**: Yes! Use GGUF quantization:
```bash
./quantize model.gguf model-Q4_K_M.gguf Q4_K_M
```

Reduces size ~10x with minimal quality loss.

See [INFERENCE.md - Quantization](INFERENCE.md#quantization).

## Troubleshooting

### "RuntimeError: CUDA out of memory"

**Answer**:
```python
# Reduce batch size
per_device_train_batch_size = 2

# Or use gradient accumulation
gradient_accumulation_steps = 4

# Or enable checkpointing
model.gradient_checkpointing_enable()
```

### "FileNotFoundError: [Errno 2] No such file or directory"

**Answer**:
1. Check file path exists
2. Verify permissions
3. Use absolute paths
4. Check working directory with `os.getcwd()`

### Tokenizer issues

**Answer**:
```python
# Ensure tokenizer is loaded
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Set pad token if needed
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
```

### Model not found on HuggingFace

**Answer**:
1. Verify model name is correct
2. Check internet connection
3. Try manual download:
   ```bash
   huggingface-cli download model_name
   ```

### Dataset format errors

**Answer**:
1. Validate format with:
   ```python
   # Check ChatML tags balance
   with open("dataset.txt") as f:
       content = f.read()
   start = content.count("<|im_start|>")
   end = content.count("<|im_end|>")
   print(f"Balanced: {start == end}")
   ```

2. Regenerate if corrupted

## Performance and Optimization

### How can I make inference faster?

**Answer**:
1. Use quantized model
2. Reduce sequence length
3. Use batch processing
4. Enable flash attention
5. Deploy on GPU

### What's the best base model to use?

**Answer**:
- **Qwen2.5-Coder**: Best for code completion
- **CodeLLaMA**: Strong code generation
- **Mistral 7B**: Good general purpose
- **Phi-3**: Small and efficient

### How do I compare model performance?

**Answer**:
1. Use same evaluation dataset
2. Measure:
   - Exact match accuracy
   - Token match rate
   - BLEU score
   - Human evaluation

3. Use metrics library:
   ```bash
   pip install evaluate
   ```

### Can I fine-tune an already fine-tuned model?

**Answer**: Yes, but:
1. Start with lower learning rate
2. May suffer from catastrophic forgetting
3. Better to combine datasets and train once

### What's the speedup with quantization?

**Answer**: Varies by method:
- Q4_K_M: 3-4x faster, minimal quality loss
- Q3_K: 4-5x faster, slight quality loss
- Q2_K: 5-6x faster, noticeable quality loss

### How much disk space do models take?

**Answer**:
- Unquantized (fp16): ~3GB for 1.5B parameters
- GGUF Q4_K_M: ~600-700MB
- LoRA adapter: 20-50MB

## Still Have Questions?

- Check [ARCHITECTURE.md](ARCHITECTURE.md) for system overview
- See individual documentation files for detailed guides
- Review code examples in the repository
- Open an issue on GitHub with your question

---

**Last Updated**: 2025-05-22
