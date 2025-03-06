from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "facebook/bart-large-mnli"

# Download and save the model locally
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model.save_pretrained("./local_model")
tokenizer.save_pretrained("./local_model")

print("Model and tokenizer saved successfully!")