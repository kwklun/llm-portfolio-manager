from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os

# Set token first
os.environ["HUGGINGFACE_TOKEN"] = "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"

# Load base model and tokenizer
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    token=os.environ["HUGGINGFACE_TOKEN"]
)

tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    token=os.environ["HUGGINGFACE_TOKEN"]
)

# Check if PEFT weights exist
peft_path = "models/fingpt_peft_weights"
model = PeftModel.from_pretrained(base_model, peft_path) if os.path.exists(peft_path) else base_model

def get_advice(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_new_tokens=100)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Test
prompt = "Given current market conditions, what is a good investment strategy?"
print(get_advice(prompt))