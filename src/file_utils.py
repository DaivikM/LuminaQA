import os
import json
import hashlib

def hash_file(file_path):
    """Generate MD5 hash of file contents."""
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def load_file_hashes(file_hashes_path):
    """Load file hashes from stored file."""
    if not os.path.exists(file_hashes_path):
        return {}
    with open(file_hashes_path, "r") as f:
        return dict(line.strip().split(",") for line in f if "," in line)

def save_file_hashes(file_hashes_path, hashes):
    """Save file hashes to file."""
    with open(file_hashes_path, "w") as f:
        for path, h in hashes.items():
            f.write(f"{path},{h}\n")

def get_documents_to_index(data_dir, file_hashes_path):
    """Identify documents that need to be indexed (new or changed)."""
    old_hashes = load_file_hashes(file_hashes_path)
    new_hashes = {}
    documents_to_index = []

    for fname in os.listdir(data_dir):
        path = os.path.join(data_dir, fname)
        if os.path.isfile(path):
            h = hash_file(path)
            new_hashes[path] = h
            if old_hashes.get(path) != h:
                documents_to_index.append(path)
                
    return documents_to_index, new_hashes

def load_conversation_history(path):
    """Load conversation history from a JSON file if it exists, else return an empty list."""
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_conversation_history(path, history):
    """Save conversation history to a JSON file, creating the file if it doesn't exist."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        json.dump(history, f, indent=2)