# Inference and Deployment Guide

Complete guide to deploying and running fine-tuned models for inference.

## Table of Contents

1. [Overview](#overview)
2. [Deployment Options](#deployment-options)
3. [Local Inference](#local-inference)
4. [Ollama Deployment](#ollama-deployment)
5. [API Deployment](#api-deployment)
6. [Quantization](#quantization)
7. [Performance Optimization](#performance-optimization)
8. [Troubleshooting](#troubleshooting)

## Overview

After fine-tuning, models can be deployed in multiple ways:

| Method | Ease | Performance | Scalability |
|--------|------|-------------|-------------|
| Local Python | Easy | Good | Limited |
| Ollama | Easy | Good | Limited |
| vLLM API | Medium | Excellent | Good |
| Cloud Deployment | Hard | Excellent | Excellent |

## Deployment Options

### 1. Local Python Inference
- **Best for**: Development, testing, single-user
- **Requirements**: GPU recommended, 8GB+ VRAM
- **Setup time**: Minutes

### 2. Ollama (Recommended for local)
- **Best for**: Local deployment, easy sharing
- **Requirements**: GPU recommended
- **Setup time**: 30 minutes

### 3. vLLM API Server
- **Best for**: Multi-user, production
- **Requirements**: GPU, cloud instance
- **Setup time**: 1-2 hours

### 4. Cloud Deployment
- **Best for**: Production, scaling
- **Platforms**: AWS, GCP, Azure, HuggingFace Spaces
- **Setup time**: 2-4 hours

## Local Inference

### Basic Python Inference

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model and tokenizer
model_path = "./path/to/fine_tuned_model"
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Prepare input
prompt = "function add(int a, int b) returns"
inputs = tokenizer(prompt, return_tensors="pt")

# Generate
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_length=256,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )

# Decode output
result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)
```

### With LoRA Adapter

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

# Load base model
base_model_path = "Qwen/Qwen2.5-1.5B-Instruct"
model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    torch_dtype=torch.float16,
    device_map="auto"
)

# Load LoRA adapter
adapter_path = "./path/to/lora_adapter"
model = PeftModel.from_pretrained(model, adapter_path)

# Merge for inference (optional but faster)
# model = model.merge_and_unload()

tokenizer = AutoTokenizer.from_pretrained(base_model_path)

# Generate
prompt = "def fibonacci(n):"
inputs = tokenizer(prompt, return_tensors="pt")

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_length=200,
        temperature=0.5
    )

result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)
```

### Generation Parameters

```python
generation_config = {
    "max_length": 256,           # Maximum tokens to generate
    "max_new_tokens": 128,       # Limit new tokens only
    "min_length": 10,            # Minimum output length
    "temperature": 0.7,          # Creativity (0=deterministic, 2=random)
    "top_p": 0.9,                # Nucleus sampling
    "top_k": 50,                 # Top-k sampling
    "do_sample": True,           # Use sampling instead of greedy
    "num_beams": 1,              # Beam search width
    "repetition_penalty": 1.1,   # Penalize repetition
    "length_penalty": 1.0,       # Length preference
    "early_stopping": False,     # Stop early if possible
}

outputs = model.generate(**inputs, **generation_config)
```

## Ollama Deployment

### Prerequisites

1. **Install Ollama**: [ollama.com](https://ollama.com)

### Step 1: Prepare Model

```bash
# If using LoRA, merge first (see below)
python -c "
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base_model = 'Qwen/Qwen2.5-1.5B-Instruct'
adapter_path = './lora_adapter'
output_path = './merged_model'

model = AutoModelForCausalLM.from_pretrained(base_model)
model = PeftModel.from_pretrained(model, adapter_path)
model = model.merge_and_unload()

model.save_pretrained(output_path)
AutoTokenizer.from_pretrained(base_model).save_pretrained(output_path)
"
```

### Step 2: Convert to GGUF

```bash
# Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make

# Convert model
python convert-hf-to-gguf.py /path/to/merged_model --outfile model.gguf
```

### Step 3: Create Modelfile

```dockerfile
FROM ./model.gguf

# Parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1
PARAMETER top_k 40

# Chat template (adjust for your model)
TEMPLATE """{{- if .Messages }}
{{- if or .System .Tools }}<|im_start|>system
{{- if .System }}
{{ .System }}
{{- end }}
{{- if .Tools }}
{{ .Tools }}
{{- end }}
<|im_end|>
{{- end }}
{{- range $i, $_ := .Messages }}
{{- if eq .Role "user" }}<|im_start|>user
{{ .Content }}<|im_end|>
{{- else if eq .Role "assistant" }}<|im_start|>assistant
{{ .Content }}<|im_end|>
{{- end }}
{{- end }}
{{- else }}
{{- if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{- end }}
{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
{{ end }}
{{ .Response }}<|im_end|>
{{- end }}
"""

# System prompt
SYSTEM "You are a helpful Ballerina code assistant."
```

### Step 4: Create Model

```bash
# In directory with Modelfile and model.gguf
ollama create ballerina-code-model -f Modelfile
```

### Step 5: Test Model

```bash
# Interactive chat
ollama run ballerina-code-model

# Or via API
curl http://localhost:11434/api/generate -d '{
  "model": "ballerina-code-model",
  "prompt": "function add(int a, int b) returns",
  "stream": false
}'
```

### Ollama API Usage

```python
import requests
import json

def query_ollama(prompt, model="ballerina-code-model"):
    """Query Ollama API"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.7,
        }
    )
    return response.json()["response"]

# Usage
result = query_ollama("function fibonacci(n: int) returns")
print(result)
```

## API Deployment

### vLLM Setup

```bash
# Install vLLM
pip install vllm

# Start server
python -m vllm.entrypoints.openai.api_server \
    --model ./path/to/model \
    --dtype float16 \
    --max-model-len 2048
```

### OpenAI-Compatible API

```python
from openai import OpenAI

# Connect to vLLM
client = OpenAI(
    api_key="your-api-key",
    base_url="http://localhost:8000/v1"
)

# Chat completion
response = client.chat.completions.create(
    model="your-model",
    messages=[
        {"role": "user", "content": "Complete this function: def add(a, b):"}
    ],
    temperature=0.7,
    max_tokens=100
)

print(response.choices[0].message.content)
```

### FastAPI Server Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI(title="Ballerina Code Completion API")

# Load model once
model = AutoModelForCausalLM.from_pretrained("./model")
tokenizer = AutoTokenizer.from_pretrained("./model")

class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7

class CompletionResponse(BaseModel):
    generated_text: str
    tokens_used: int

@app.post("/complete", response_model=CompletionResponse)
async def complete(request: CompletionRequest):
    """Generate code completion"""
    try:
        inputs = tokenizer(request.prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=request.max_tokens,
                temperature=request.temperature
            )
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return CompletionResponse(
            generated_text=result,
            tokens_used=outputs[0].shape[0]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Run with: uvicorn app:app --host 0.0.0.0 --port 8000
```

## Quantization

### GGUF Quantization

```bash
# Using llama.cpp
./quantize model.gguf model-Q4_K_M.gguf Q4_K_M
```

**Quantization Levels**:
```
Q2_K     → ~2.3 bits (poorest quality, smallest)
Q3_K_S   → ~3.5 bits
Q3_K_M   → ~3.5 bits (balanced)
Q3_K_L   → ~3.5 bits (larger, better)
Q4_K_S   → ~4.3 bits
Q4_K_M   → ~4.3 bits (recommended)
Q5_K_S   → ~5.5 bits
Q5_K_M   → ~5.5 bits
Q6_K     → ~6.6 bits (better quality, larger)
Q8_0     → ~8.5 bits (near-original quality)
```

### 8-bit Quantization (PyTorch)

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

# 8-bit quantization config
quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    bnb_8bit_compute_dtype=torch.float16
)

model = AutoModelForCausalLM.from_pretrained(
    "model_path",
    quantization_config=quantization_config,
    device_map="auto"
)
```

## Performance Optimization

### GPU Memory Optimization

```python
# Enable flash attention
model.config.use_flash_attention_2 = True

# Use lower precision
torch_dtype = torch.float16

# Smaller batch for streaming
batch_size = 1
```

### Batch Processing

```python
prompts = [
    "function add(int a, int b) returns",
    "service / on new http:Listener(9090) {",
    "type Person record {"
]

inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True)

with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=50)

results = tokenizer.batch_decode(outputs, skip_special_tokens=True)
```

### Streaming Output

```python
from transformers import TextIteratorStreamer
from threading import Thread

streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True)

inputs = tokenizer("function ", return_tensors="pt")

generation_kwargs = dict(
    inputs,
    streamer=streamer,
    max_new_tokens=100,
)

# Run generation in thread
thread = Thread(target=model.generate, kwargs=generation_kwargs)
thread.start()

# Stream output
for text in streamer:
    print(text, end="", flush=True)
```

## Troubleshooting

### Model Not Found

**Solution**:
```bash
# Verify model path
ls -la ./path/to/model
# Check files: config.json, model.safetensors, tokenizer.json
```

### Out of Memory During Inference

**Solutions**:
```python
# Use lower precision
torch_dtype = torch.float16

# Reduce max_length
outputs = model.generate(..., max_new_tokens=50)

# Use smaller batch size
batch_size = 1

# Enable memory-efficient attention
model.config.use_flash_attention_2 = True
```

### Slow Generation

**Solutions**:
1. Use quantized model (faster)
2. Reduce sequence length
3. Use batch processing for multiple prompts
4. Enable flash attention
5. Use GPU instead of CPU

### Ollama Connection Issues

**Solution**:
```bash
# Check if running
ollama list

# Start Ollama server
ollama serve

# Test API
curl http://localhost:11434/api/tags
```

## Deployment Checklist

- [ ] Model merged (if using LoRA)
- [ ] Converted to target format (GGUF for Ollama)
- [ ] Quantization applied (if needed)
- [ ] API server configured
- [ ] Authentication setup (if public)
- [ ] Rate limiting configured
- [ ] Monitoring setup
- [ ] Load testing completed
- [ ] Error handling tested
- [ ] Documentation updated

---

For training, see [TRAINING.md](TRAINING.md).
For model building, see [models/README.md](../models/README.md).
