from transformers import AutoConfig

# Replace 'model_name_or_path' with the actual model name or path
model_name_or_path = 'sentence-transformers/distiluse-base-multilingual-cased-v1'
# https://huggingface.co/sentence-transformers/distiluse-base-multilingual-cased-v1/resolve/main/config.json

# Load the model configuration
config = AutoConfig.from_pretrained(model_name_or_path)

# Print the revision number
print(f"Revision: {config.transformers_version}")