import os
import json
import html
import re
from typing import Any

input_file = "temp/trn.json"
output_file = "output/titles_and_contents.json"
invalid_output = "output/invalid_titles_and_contents.json"


def smart_space(text):
    # Add space before capital letter only if followed by lowercase (not for acronyms)
    text = re.sub(r"(?<=[a-z])([A-Z])", r" \1", text)
    # Optionally, fix cases where a number follows a letter (e.g., "Instructions100%")
    text = re.sub(r"(?<=[a-zA-Z])([0-9])", r" \1", text)
    # Ensure proper spacing after periods if followed by a upper case letter
    text = re.sub(r"\.(?=[A-Z])", ". ", text)
    # Ensure proper spacing after question marks if followed by a upper case letter
    text = re.sub(r"\?(?=[A-Z])", "? ", text)
    return text


def clean_and_standardize_text(text: str) -> str:
    """
    Clean and normalize text for NLP/fine-tuning.
    - Unescapes HTML entities
    - Replaces problematic unicode and typographic characters
    - Normalizes whitespace
    - Removes control characters
    """
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    # Replace common problematic characters
    replacements = {
        "\t": " ",
        "\u00a0": " ",
        "“": '"',
        "”": '"',
        "‘": "'",
        "‚": ",",
        "’": "'",
        "´": "'",
        "—": "-",
        "–": "-",
        "¿": "-",
        "¹": "'",
        "‹": "-",
        "›": "-",
        "³": '"',
        "²": '"',
        "Â": "",
        "â€": " ",
        "*": "-",
        "•": "-",
        "_": "-",
        "·": "-",
        "®": "",
        "™": "",
        "�": "",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Remove any remaining control characters except newlines
    text = re.sub(r"[\x00-\x09\x0b-\x1f\x7f]", "", text)
    # Remove leading whitespace, dots, and commas
    text = re.sub(r"^[\s.,]+", "", text)
    # Collapse multiple hyphens into a single hyphen
    text = re.sub(r"-{2,}", "-", text)
    # Replace multiple question marks with a single question mark
    text = re.sub(r"\?{2,}", "?", text)
    # Replace period followed by question mark with a single period
    text = re.sub(r"\.\?", ".", text)
    # Insert spaces
    text = smart_space(text)
    # Normalize whitespace (collapse multiple spaces, remove leading/trailing)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_repeated_char(text: str, min_length: int = 2) -> bool:
    """Return True if text (ignoring whitespace) is only one unique character and at least min_length long."""
    return len(text) >= min_length and len(set(text)) == 1


def is_number(text: str) -> bool:
    """Return True if text is a number (integer or float)."""
    return text.isnumeric()


def is_empty(text: str) -> bool:
    """Return True if text is empty or only whitespace."""
    return not text or len(text) == 0


def is_not_applicable(text: str) -> bool:
    """Return True if text is 'N/A' (case insensitive) after stripping whitespace."""
    return text.lower() == "n/a" or text.lower() == "na"


def has_letters(text: str) -> bool:
    return bool(re.search(r"\w", text, re.UNICODE))


def is_valid_title(title: str) -> bool:
    """Return True if text is not empty, not a single char, and not repeated char string."""
    return not (is_empty(title) or is_repeated_char(title) or is_not_applicable(title))


def is_valid_content(content: str) -> bool:
    """Return True if text is not empty, not a single char, and not repeated char string."""
    return not (
        is_empty(content)
        or is_repeated_char(content)
        or is_number(content)
        or is_not_applicable(content)
    ) and has_letters(content)


def process_json_lines(input_path: str, output_path: str) -> None:
    """Process NDJSON file, clean and filter entries, and write valid ones to output."""
    count = 0
    valid = 0
    try:
        # Ensure the output directory exists
        os.makedirs("output", exist_ok=True)
        with open(input_path, "r", encoding="utf-8") as fin, open(
            output_path, "w", encoding="utf-8"
        ) as fout, open(invalid_output, "w", encoding="utf-8") as ferr:
            for line in fin:
                if line.strip():
                    try:
                        obj: Any = json.loads(line)
                        title = clean_and_standardize_text(obj.get("title", ""))
                        content = clean_and_standardize_text(obj.get("content", ""))
                        if is_valid_title(title) and is_valid_content(content):
                            new_obj = {"title": title, "content": content}
                            fout.write(json.dumps(new_obj, ensure_ascii=False) + "\n")
                            valid += 1
                        else:
                            ferr.write(json.dumps({"title": title, "content": content}, ensure_ascii=False) + "\n")
                    except Exception as e:
                        print(f"Error processing line {count + 1}: {e}")
                count += 1
                if count % 1000 == 0:
                    print(f"Processed {count} lines - {valid} valid entries - {count - valid} invalid entries.")
        print(f"Done! Total lines processed: {count} - valid entries: {valid} - invalid entries: {count - valid}")
        print(f"Valid entries written to: {output_path}")
        print(f"Invalid entries written to: {invalid_output}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    process_json_lines(input_file, output_file)
