# Training Guide

Complete guide to fine-tuning models using both SFT and LoRA approaches.

## Table of Contents

1. [Overview](#overview)
2. [Training Approaches](#training-approaches)
3. [SFT Training](#sft-training)
4. [LoRA Training](#lora-training)
5. [Hyperparameters](#hyperparameters)
6. [Monitoring Training](#monitoring-training)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## Overview

The project supports two fine-tuning approaches:

| Aspect | SFT | LoRA |
|--------|-----|------|
| **Memory Usage** | 🔴 High | 🟢 Low |
| **Training Time** | 🟡 Longer | 🟢 Fast |
| **Model Performance** | 🟢 Better | 🟡 Good |
| **Deployment Size** | 🔴 Large | 🟢 Small |
| **Computational Cost** | 🔴 High | 🟢 Low |
| **Use Case** | Maximum performance | Resource-constrained |

## Training Approaches

### Supervised Fine-Tuning (SFT)

**What it does**: Updates all model weights during training.

**When to use**:
- Maximum model performance is needed
- Sufficient GPU memory available (12GB+)
- Training time is not a critical constraint
- Target a specific narrow domain

**Pros**:
- Better model performance
- More complete adaptation
- No adapter merging needed

**Cons**:
- High memory requirements
- Longer training time
- Larger resulting models
- Difficult to maintain multiple versions

### Low-Rank Adaptation (LoRA)

**What it does**: Trains only small adapter layers while keeping base model frozen.

**When to use**:
- Limited GPU memory (6GB+)
- Need fast training
- Want multiple specialized model variants
- Need efficient deployment

**Pros**:
- Low GPU memory requirements (50-75% reduction)
- Fast training (2-3x speedup)
- Small adapter files (5-50MB)
- Easy to maintain multiple adapters

**Cons**:
- Slightly lower performance than SFT
- Requires adapter merging for inference
- More complex deployment

## SFT Training

### Environment Setup

```bash
cd training/SFT/Tweets
# or
cd training/SFT/Kagggle
```

### Basic Training Script

```python
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset

# Load model and tokenizer
model_name = "Qwen/Qwen2.5-1.5B-Instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load dataset
dataset = load_dataset("text", data_files={
    "train": "../data/chatML/train_*.txt",
    "validation": "../data/chatML/val_*.txt"
})

# Tokenize dataset
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=512
    )

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    num_proc=4
)

# Training arguments
training_args = TrainingArguments(
    output_dir="./sft_output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    save_steps=500,
    eval_steps=500,
    learning_rate=2e-4,
    lr_scheduler_type="linear",
    save_total_limit=3,
    push_to_hub=False
)

# Training
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    data_collator=DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
)

trainer.train()

# Save model
model.save_pretrained("./sft_model_final")
tokenizer.save_pretrained("./sft_model_final")
```

### Configuration for SFT

```python
# Memory optimization
model.gradient_checkpointing_enable()

training_args = TrainingArguments(
    # Memory optimization
    gradient_accumulation_steps=2,
    gradient_checkpointing=True,
    fp16=True,  # Mixed precision training
    
    # Learning rate
    learning_rate=2e-4,
    warmup_steps=500,
    
    # Batch size
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    
    # Training duration
    num_train_epochs=3,
    max_steps=-1,
    
    # Optimization
    optim="paged_adamw_8bit",  # 8-bit optimizer for memory
    
    # Logging
    logging_steps=10,
    save_steps=500,
    eval_steps=500,
)
```

## LoRA Training

### Environment Setup

```bash
cd training/LoRA

# Install PEFT
pip install peft
```

### Basic LoRA Training Script

```python
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import get_peft_model, LoraConfig, TaskType
from datasets import load_dataset

# Load model and tokenizer
model_name = "Qwen/Qwen2.5-1.5B-Instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# LoRA configuration
lora_config = LoraConfig(
    r=8,                           # Rank
    lora_alpha=16,                 # Alpha scaling
    target_modules=["q_proj", "v_proj"],  # Target modules
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Load and prepare dataset
dataset = load_dataset("text", data_files={
    "train": "../data/chatML/train_*.txt",
    "validation": "../data/chatML/val_*.txt"
})

def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=512
    )

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    num_proc=4
)

# Training arguments
training_args = TrainingArguments(
    output_dir="./lora_output",
    num_train_epochs=3,
    per_device_train_batch_size=8,  # Can use larger batch with LoRA
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    save_steps=500,
    eval_steps=500,
    learning_rate=5e-4,  # Higher LR for LoRA
    lr_scheduler_type="cosine"
)

# Training
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    data_collator=DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
)

trainer.train()

# Save LoRA adapter
model.save_pretrained("./lora_adapter")
tokenizer.save_pretrained("./lora_adapter")
```

### LoRA Configuration

```python
lora_config = LoraConfig(
    # Model architecture
    r=8,                    # Rank of adaptation matrices
    lora_alpha=16,          # Scaling factor (alpha/r)
    
    # Modules to apply LoRA
    target_modules=["q_proj", "v_proj", "k_proj"],
    
    # Regularization
    lora_dropout=0.05,
    
    # Training settings
    bias="none",            # "none" | "all" | "lora_only"
    task_type=TaskType.CAUSAL_LM,
    
    # For multi-GPU
    modules_to_save=None,
)
```

## Hyperparameters

### Learning Rate

```python
# SFT: Generally lower
learning_rate = 2e-4

# LoRA: Can be higher
learning_rate = 5e-4

# Warmup
warmup_steps = 500
warmup_ratio = 0.1  # Alternative: warmup as ratio of total
```

### Batch Size

```python
# SFT (memory constrained)
per_device_train_batch_size = 4
gradient_accumulation_steps = 2

# LoRA (more memory efficient)
per_device_train_batch_size = 8
gradient_accumulation_steps = 1
```

### Training Duration

```python
# Number of epochs
num_train_epochs = 3

# Alternative: max steps
max_steps = 5000

# Evaluation frequency
eval_steps = 500
save_steps = 500
```

### Optimization

```python
# Optimizer
optim = "paged_adamw_8bit"  # For SFT with memory constraints
optim = "adamw_torch"       # Standard (for LoRA)

# Learning rate scheduler
lr_scheduler_type = "linear"     # Linear warmup
lr_scheduler_type = "cosine"     # Cosine annealing
```

## Monitoring Training

### Using ResourceMonitor

```python
from utils.fine_tuning_profiler import ResourceMonitor

# Initialize monitor
monitor = ResourceMonitor(
    interval=5,              # Check every 5 seconds
    log_path="training_metrics.csv",
    verbose=True
)

# Start monitoring
monitor.start()

# Run training
trainer.train()

# Stop monitoring
monitor.stop()

# Analyze results
metrics = monitor.get_resource_log()
print(monitor.get_summary())

# Visualize
monitor.plot_metrics()
```

### Training Metrics

Monitor these key metrics:

```
Training Loss       → Should decrease smoothly
Validation Loss     → Should decrease, watch for overfitting
Learning Rate       → Should follow configured schedule
GPU Memory          → Should plateau after initial allocation
GPU Utilization     → Should be >80% during training
Training Speed      → Samples/second or tokens/second
```

### TensorBoard Visualization

```bash
# During training
tensorboard --logdir=./logs

# Access at http://localhost:6006
```

## Best Practices

### 1. Data Preparation

```python
# Do:
- Use diverse, high-quality code samples
- Ensure proper train/val/test splits
- Validate data formatting

# Don't:
- Mix languages or frameworks
- Include commented-out code without context
- Train and evaluate on same data
```

### 2. Model Selection

```python
# Recommended base models for code
- Qwen2.5-Coder (best for code completion)
- CodeLLaMA (strong code generation)
- Mistral 7B (general purpose)
- Phi-3 (small, efficient)
```

### 3. Hyperparameter Selection

```python
# Start with baseline
learning_rate = 2e-4 (SFT) or 5e-4 (LoRA)
batch_size = 4 (SFT) or 8 (LoRA)
num_epochs = 3

# Adjust based on results
- If validation loss not decreasing: lower learning_rate or use warmup
- If loss oscillating: reduce learning_rate or batch_size
- If training slow: increase batch_size (if memory allows)
- If overfitting: reduce epochs or add dropout
```

### 4. Checkpointing

```python
training_args = TrainingArguments(
    save_strategy="steps",
    save_steps=500,
    save_total_limit=3,           # Keep only 3 checkpoints
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss"
)
```

### 5. GPU Memory Management

```python
# Enable gradient checkpointing
model.gradient_checkpointing_enable()

# Use 8-bit optimizer
optim = "paged_adamw_8bit"

# Mixed precision training
fp16 = True
fp16_opt_level = "O2"
```

## Troubleshooting

### Out of Memory (OOM)

**Solution**:
```python
# Reduce batch size
per_device_train_batch_size = 2

# Enable gradient checkpointing
model.gradient_checkpointing_enable()

# Use 8-bit optimizer
optim = "paged_adamw_8bit"

# Increase gradient accumulation
gradient_accumulation_steps = 4
```

### Training Loss Not Decreasing

**Solutions**:
1. Check data loading and preprocessing
2. Lower learning rate: `2e-5` instead of `2e-4`
3. Increase warmup steps: `1000` instead of `500`
4. Verify batch size is reasonable
5. Check if model is properly loaded

### Validation Loss Increasing (Overfitting)

**Solutions**:
```python
# Reduce training epochs
num_train_epochs = 1

# Add early stopping
early_stop_callback = EarlyStoppingCallback(
    early_stopping_patience=3,
    early_stopping_threshold=0.001
)

# Reduce model complexity
# Use LoRA with smaller rank
r = 4
```

### Training Very Slow

**Solutions**:
1. Increase batch size (if memory allows)
2. Use mixed precision: `fp16=True`
3. Reduce sequence length if possible
4. Use distributed training with `accelerate`

### CUDA Errors

**Solution**:
```bash
# Clear cache
python -c "import torch; torch.cuda.empty_cache()"

# Check GPU status
nvidia-smi

# Restart training with fresh GPU
```

## Performance Benchmarks

### SFT on 1.5B Model

```
Batch Size: 4
GPU: NVIDIA A100 (80GB)
Dataset: ~10k examples
Time per epoch: ~2 hours
Total training time (3 epochs): ~6 hours
Final model size: ~3GB
```

### LoRA on 1.5B Model

```
Batch Size: 8
GPU: NVIDIA RTX 3090 (24GB)
Dataset: ~10k examples
Time per epoch: ~30 minutes
Total training time (3 epochs): ~1.5 hours
Adapter size: ~20MB
```

---

For data preparation, see [DATA_PROCESSING.md](DATA_PROCESSING.md).
For deployment, see [INFERENCE.md](INFERENCE.md).
