# # from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# # import os
# from sentence_transformers import SentenceTransformer

# # def download_model(model_path, model_name):
# #     """Download a Hugging Face model and tokenizer to the specified directory"""
# #     # Check if the directory already exists
# #     if not os.path.exists(model_path):
# #         # Create the directory
# #         os.makedirs(model_path)

# #     tokenizer = AutoTokenizer.from_pretrained(model_name)
# #     model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# #     # Save the model and tokenizer to the specified directory
# #     model.save_pretrained(model_path)
# #     tokenizer.save_pretrained(model_path)

# # download_model("sentence-transformers", "sentence-transformers/distiluse-base-multilingual-cased-v1")

# model = SentenceTransformer("distiluse-base-multilingual-cased-v1")
# model.save(modelPath)
