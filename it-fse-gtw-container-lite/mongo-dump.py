from os import getenv, path, mkdir, remove
from shutil import rmtree, copyfileobj
from urllib.request import urlopen
from dotenv import load_dotenv
import gzip

load_dotenv()

# VARIABLES
MONGO_DUMP_URL = getenv("MONGO_DUMP_URL")
FILES = ["schema.json.gzip", "schematron.json.gzip", "terminology.json.gzip", "transform.json.gzip"]
SCRIPT_DIR = path.dirname(path.abspath(__file__))
FOLDER = path.join(SCRIPT_DIR, "../mongo-dump")

if MONGO_DUMP_URL is None:
    raise ValueError("MONGO_DUMP_URL environment variable is not set in .env")

# CHECK if folder already exists, if yes it will be deleted
if path.exists(FOLDER):
    rmtree(FOLDER)
    print(" - mongo-dump folder already exists. It will be deleted and recreated.")

# CREATE mongo folder
mkdir(FOLDER)
print(" - mongo-dump folder has been created.")

for file in FILES:
    url = f"{MONGO_DUMP_URL}/{file}"
    print(f"{file.upper()}")
    print(f" - HTTP request for {file} is starting: {url}")
    response = urlopen(url)
    print(f" - {file} is downloaded.")

    # Salva il file compresso
    compressed_path = path.join(FOLDER, file)
    with open(compressed_path, "wb") as f:
        print(f" - {file} in writing...")
        f.write(response.read())
        print(f" - {file} is written on disk.")

    # Decomprimi il file: il nome del file decomprimato sarà lo stesso senza l'estensione .gzip
    decompressed_filename = file.replace(".gzip", "")
    decompressed_path = path.join(FOLDER, decompressed_filename)
    with gzip.open(compressed_path, 'rb') as f_in:
        with open(decompressed_path, 'wb') as f_out:
            copyfileobj(f_in, f_out)
    print(f" - {file} is decompressed to {decompressed_filename}.")
    remove(compressed_path)
    print(f" - {file} compressed file is removed.")
