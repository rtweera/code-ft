# Model building README

## Merge Adapter Weights (if applicable)

If your fine-tuning used LoRA or adapters, you need to merge the adapter weights (`adapter_model.safetensors`) with the base model weights. Here’s how:

1. **Install Dependencies**:

    ```bash
    pip install transformers torch peft
    ```

2. **Merge the Weights**:
    Use a Python script to combine the base model and adapter weights. Replace `BASE_MODEL_PATH` with the path to the original Qwen 2.5B model (download it from Hugging Face if needed).

    ```python
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    # Paths
    base_model_path = "Qwen/Qwen2.5-1.5B-Instruct"  # Adjust to the correct base model
    adapter_path = "ollama-finetuned-qwen"  # Path/directory to your adapter model files
    output_path = "merged-qwen2.5-finetuned"

    # Load base model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(base_model_path)
    tokenizer = AutoTokenizer.from_pretrained(base_model_path)

    # Load and apply the adapter
    model = PeftModel.from_pretrained(model, adapter_path)
    model = model.merge_and_unload()  # Merge adapter into base model

    # Save the merged model
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    ```

    This will create a new directory (`merged-qwen2.5-finetuned`) with the full merged weights.

## Export to Ollama steps

1. Create a `Modelfile` in the model directory. This file contains metadata about the model and how to load it. Here’s a basic example:

    ```yaml
    FROM ./qwen2.5-finetuned.gguf

    # Define the template (based on Qwen2.5-Coder’s FIM and chat capabilities)
    TEMPLATE """{{- if .Suffix }}<|fim_prefix|>{{ .Prompt }}<|fim_suffix|>{{ .Suffix }}<|fim_middle|>
    {{- else if .Messages }}
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
    {{ .Content }}<|im_end>
    {{- else if eq .Role "assistant" }}<|im_start|>assistant
    {{ .Content }}<|im_end>
    {{- end }}
    {{- end }}
    {{- else }}
    <|im_start|>user
    {{ .Prompt }}<|im_end>
    <|im_start|>assistant
    {{ .Response }}<|im_end>
    {{- end }}
    """

    # Optional parameters
    PARAMETER temperature 0.7
    PARAMETER top_p 0.8
    PARAMETER repeat_penalty 1.05
    PARAMETER top_k 20

    # System prompt
    SYSTEM "You are a fine-tuned Qwen2.5-Coder 0.5B model, optimized for coding assistance."
    ```

    > **Note:** Adjust the `FROM` path to point to your GGUF file. The `TEMPLATE` is based on Qwen2.5-Coder’s chat format; modify it if your fine-tuning changed the expected input/output style.

2. Create the model in Ollama. Run the following command in the directory containing your `Modelfile` and `qwen2.5-finetuned.gguf`:

    ```bash
        ollama create my-qwen-finetuned -f Modelfile
    ```

3. Run the model:

    ```bash
        ollama run my-qwen-finetuned
    ```
