# API-Based Inference Setup Guide

This guide explains how to evaluate models served via vLLM API server (with LoRA support) using the unified evaluator.

## Changes Made

### 1. Modified Files
- `vendor/goedel-prover/src/inference.py` - Added support for OpenAI-compatible API calls
- `scripts/run_minif2f.py` - Added API parameter forwarding
- `evaluators/minif2f_evaluator.py` - Added model config API parameter extraction
- `utils/config_loader.py` - Added support for `location: "api"` type

### 2. Backup Files Created
- `vendor/goedel-prover/src/inference.py.backup`
- `scripts/run_minif2f.py.backup`
- `evaluators/minif2f_evaluator.py.backup`
- `utils/config_loader.py.backup`

## Usage

### Step 1: Start Your vLLM Server

Your vLLM server should already be running with:
```bash
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen3-32B \
    --enable-lora \
    --lora-modules \
        prover=/scratch/shared_dir/lora/qwen/prover_sanitized \
    --port 8000 \
    --max-loras 5 \
    --max-lora-rank 128 \
    --gpu-memory-utilization 0.85
```

### Step 2: Update config.yml

Your `config.yml` has been updated with the following configuration:

```yaml
models:
  - model_name: "prover"  # Matches your LoRA adapter name
    path: "Qwen/Qwen3-32B"  # Base model (for display)
    type: "base"
    description: "Prover model with LoRA via vLLM server"
    location: "api"  # REQUIRED: Tells the evaluator to use API mode
    # API-specific settings (REQUIRED)
    api_base: "http://localhost:8000/v1"
    api_model_name: "prover"  # Must match --lora-modules name
    tokenizer_path: "Qwen/Qwen3-32B"  # For prompt formatting
```

**Important Fields**: 
- `location: "api"` - Required to enable API mode
- `api_base` - OpenAI-compatible endpoint URL
- `api_model_name` - Must match the name in your `--lora-modules` argument (in this case, "prover")
- `tokenizer_path` - Path to the base model tokenizer for proper prompt formatting

### Step 3: Run Evaluation

```bash
python unified_evaluator.py --config config.yml
```

Or use the example config:
```bash
python unified_evaluator.py --config config_api_example.yml
```

## How It Works

1. **Config Loading**: `utils/config_loader.py` recognizes `location: "api"` and validates that `api_base` is present
2. **Model Configuration**: The evaluator passes API parameters from model config to the minif2f evaluator
3. **Command Construction**: `minif2f_evaluator.py` extracts API settings and passes them to `run_minif2f.py`
4. **Script Execution**: `run_minif2f.py` forwards API parameters to `inference.py`
5. **Inference**: When `--api_base` is specified, `inference.py` uses OpenAI client instead of loading model locally
6. **API Calls**: HTTP requests are made to your vLLM server with the specified `api_model_name` to use the LoRA adapter

## Troubleshooting

### Error: "Unknown location type 'api'"
Make sure you've updated `utils/config_loader.py` with the changes. The backup should be at `utils/config_loader.py.backup`.

### Error: "Missing 'api_base' field"
Your model config must include the `api_base` field when using `location: "api"`.

### OpenAI Package Not Found
If you get an import error for `openai`, install it:
```bash
pip install openai
```

### Connection Refused
Make sure your vLLM server is running and accessible at the specified `api_base` URL:
```bash
curl http://localhost:8000/v1/models
```

You should see a JSON response listing available models, including your LoRA adapter name.

### Wrong LoRA Adapter Used
Verify that `api_model_name` exactly matches the name in your `--lora-modules` argument:
- Server: `--lora-modules prover=/path/to/lora`
- Config: `api_model_name: "prover"`

### Tokenizer Issues
If you get tokenizer errors, make sure `tokenizer_path` points to a valid model directory with tokenizer files. This can be:
- A local path: `/path/to/model`
- A HuggingFace model ID: `Qwen/Qwen3-32B`

## Testing the Setup

### 1. Verify vLLM Server is Running
```bash
curl http://localhost:8000/v1/models
```

### 2. Test API Call Manually
```bash
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "prover",
    "prompt": "theorem test : 1 + 1 = 2 := by",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

### 3. Run a Small Test
Modify `config.yml` to test with just 2 samples:
```yaml
minif2f_settings:
  num_samples: 2  # Reduced for testing
```

## Reverting Changes

If you need to revert to the original code:
```bash
cp vendor/goedel-prover/src/inference.py.backup vendor/goedel-prover/src/inference.py
cp scripts/run_minif2f.py.backup scripts/run_minif2f.py
cp evaluators/minif2f_evaluator.py.backup evaluators/minif2f_evaluator.py
cp utils/config_loader.py.backup utils/config_loader.py
```

## Example Configs

### Local Model (Original)
```yaml
models:
  - model_name: "my-model"
    path: "/path/to/local/model"
    type: "base"
    location: "local"
```

### HuggingFace Model
```yaml
models:
  - model_name: "hf-model"
    path: "meta-llama/Llama-2-7b-hf"
    type: "base"
    location: "hf"
```

### API Model (with LoRA)
```yaml
models:
  - model_name: "prover"
    path: "Qwen/Qwen3-32B"
    type: "base"
    location: "api"
    api_base: "http://localhost:8000/v1"
    api_model_name: "prover"
    tokenizer_path: "Qwen/Qwen3-32B"
```
