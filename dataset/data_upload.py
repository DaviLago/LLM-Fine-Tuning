import os
import json
from datasets import Dataset
from huggingface_hub import login
from dotenv import load_dotenv

# Login to Hugging Face
load_dotenv()
login(token=os.environ["HF_TOKEN"])

# Load the processed data
data = []
with open("output/titles_and_contents.json", "r", encoding="utf-8") as f:
    for line in f:
        if line:
            data.append(json.loads(line))

# Create a Dataset object
dataset = Dataset.from_list(data)

# Set your desired repo name
repo_id = "DaviLago/AmazonTitles-1.3MM"

# Push to the Hugging Face Hub
dataset.push_to_hub(repo_id)
