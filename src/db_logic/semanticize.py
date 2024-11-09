# Load model directly
from transformers import AutoTokenizer, AutoModel, pipeline
import torch

# Load the HF_TOKEN from the .env file
from dotenv import load_dotenv
import os
load_dotenv()

tokenizer = AutoTokenizer.from_pretrained(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
model = AutoModel.from_pretrained(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
pipeline_generation_keywords = pipeline("text-generation", model='meta-llama/Llama-3.2-1B-Instruct', torch_dtype=torch.bfloat16, token=os.getenv("HF_TOKEN"))


def generate_semantic_vector(text: str):
    """
    To use this function, you can just call it with any text and it will return the semantic vector for that text
    """
    # First, generate the keywords of the text
    chat_template = [
        {
            "role": "system",
            "content": "From the following text, given by the user, extract a list of specific keywords related to the topic",
        },
        {"role": "user", "content": text},
    ]
    generated_keywords = pipeline_generation_keywords(chat_template, max_new_tokens=100)[0]["generated_text"][-1]['content']

    print(f"Generated keywords: {generated_keywords}")

    inputs = tokenizer(
        generated_keywords, return_tensors="pt", padding=True, truncation=True, max_length=512
    )
    outputs = model(**inputs)
    last_layer_states = outputs[0]
    # Sum and divide by the number of tokens
    pooled_output = last_layer_states.sum(axis=1).mul(1.0 / last_layer_states.shape[1])
    return pooled_output.squeeze().tolist()
