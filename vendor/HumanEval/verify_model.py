import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import traceback
import os

# --- Configuration: Please set your model paths here ---

# 1. Base Model (which we know is working correctly)
BASE_MODEL_PATH = "/scratch/shared_dir/xinyu/DeepSeek-Coder-V2-Lite-Instruct"

# 2. The fine-tuned model from your teammate (which we suspect is faulty)
FINETUNED_MODEL_PATH = "/scratch/shared_dir/xinyu/FFT-instruct-V2-Golang"
# ---------------------------------------------------------

def check_path_exists(path, model_name):
    """Checks if the specified path exists."""
    print(f"Checking if path exists for '{model_name}': '{path}'")
    if not os.path.isdir(path):
        print(f"❌ ERROR: Directory not found at the specified path.\n")
        return False
    print(f"✅ Path found.\n")
    return True

def test_model_loading(model_path, model_name):
    """
    Attempts to load the tokenizer and model from a given path and reports the result.
    """
    print(f"--- Verifying Model: {model_name} ---")
    
    if not check_path_exists(model_path, model_name):
        return

    try:
        # Step 1: Attempt to load the Tokenizer
        print("▶️  Step 1/2: Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        print("✅ Tokenizer loaded successfully!\n")

        # Step 2: Attempt to load the Model weights
        print("▶️  Step 2/2: Loading model...")
        # Using bfloat16 and device_map='auto' to simulate a realistic multi-GPU loading environment
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        print("✅ Model loaded successfully!")

        print(f"\n[ RESULT ] 🟢 {model_name}: PASSED. Tokenizer and model loaded without errors.\n")

    except Exception as e:
        # If an exception occurs during any step, catch it and print the details
        print(f"\n[ RESULT ] 🔴 {model_name}: FAILED. An error occurred during the loading process.")
        print("-------------------- ERROR DETAILS --------------------")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        print("\nFull Traceback:")
        # Print the full Python traceback, which is crucial for debugging
        traceback.print_exc()
        print("------------------------------------------------------\n")


if __name__ == "__main__":
    # Run the verification tests
    test_model_loading(BASE_MODEL_PATH, "Original Base Model (DeepSeek Coder V2)")
    
    # Print a separator for clear-cut results
    print("\n" + "="*80 + "\n") 
    
    test_model_loading(FINETUNED_MODEL_PATH, "Teammate's Fine-tuned Model (Golang)")