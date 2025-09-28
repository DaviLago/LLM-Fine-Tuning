import gdown
import zipfile
import gzip
import os
import shutil

# Google Drive file ID
file_id = "12zH4mL2RX8iSvH0VCNnd3QxO4DzuHWnK"

# Paths
zip_path = "temp/LF-Amazon-1.3M.raw.zip"
extract_dir = "temp"
gz_file = os.path.join(extract_dir, "trn.json.gz")
json_file = os.path.join(extract_dir, "trn.json")
target_file = "LF-Amazon-1.3M/trn.json.gz"

# Ensure the temp directory exists
os.makedirs("temp", exist_ok=True)

# Download the file
gdown.download(f"https://drive.google.com/uc?id={file_id}", zip_path, quiet=False)

# Extract trn.json.gz from zip
with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extract(target_file, "temp")
    # Move to the correct directory
    os.makedirs(extract_dir, exist_ok=True)
    src = os.path.join("temp", target_file)
    shutil.move(src, gz_file)

# Extract trn.json from trn.json.gz
with gzip.open(gz_file, "rb") as f_in, open(json_file, "wb") as f_out:
    shutil.copyfileobj(f_in, f_out)

print(f"Extracted: {json_file}")

# Remove temporary files and directories
os.remove(zip_path)
os.remove(gz_file)
shutil.rmtree("temp/LF-Amazon-1.3M")
