# LLM Fine-Tuning: Llama-2-7b-hf on Amazon Titles Dataset

This project demonstrates how to fine-tune the Llama-2-7b-hf language model using a dataset of Amazon product titles and descriptions. The workflow includes data processing, uploading, and model fine-tuning, as well as a notebook for comparing the base and fine-tuned models.

## Project Structure

```
dataset/
├── data_processor.py         # Script for processing raw dataset
├── data_upload.py            # Script for uploading processed data
├── download_raw_dataset.py   # Script to download the raw dataset
├── output/
│   ├── invalid_titles_and_contents.json
│   └── titles_and_contents.json
└── temp/
    └── trn.json              # Training data in JSON format
fine-tuning/
├── llm_fine_tuning.ipynb             # Notebook for fine-tuning the model
└── llm_fine_tuning_comparison.ipynb  # Notebook comparing base and fine-tuned models
LICENSE
requirements.txt
```

## Setup

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Prepare the dataset**
   - Use `download_raw_dataset.py` to download the raw data.
   - Process the data with `data_processor.py`.
   - Upload or move the processed data as needed using `data_upload.py`.

4. **Fine-tune the model**
   - Open `fine-tuning/llm_fine_tuning.ipynb` and follow the steps to fine-tune Llama-2-7b-hf using the processed dataset.

5. **Compare results**
   - Use `fine-tuning/llm_fine_tuning_comparison.ipynb` to compare outputs from the base and fine-tuned models on sample prompts.

## Notebooks

- **llm_fine_tuning.ipynb**: Guides you through the process of loading data, configuring the model, and running the fine-tuning process.
- **llm_fine_tuning_comparison.ipynb**: Compares the outputs of the base and fine-tuned models using a sample product title prompt.

## Data

- The dataset consists of Amazon product titles and their corresponding descriptions, stored in JSON format in `dataset/output/` and `dataset/temp/`.

## Model

- **Base Model**: `meta-llama/Llama-2-7b-hf`
- **Fine-Tuned Adapter**: `DaviLago/amazon-titles-llama-finetuned`

## License

See [LICENSE](LICENSE) for details.
