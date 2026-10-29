import json
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading smoldata.json...")
with open("smoldata.json") as f:
    data = json.load(f)
pages = data["pages"]
print(f"{len(pages)} pages to embed")

print("Loading model all-MiniLM-L6-v2...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# embed title + text, in the same order as pages
texts = [f"{p[0]}. {p[2]}" for p in pages]
print("Embedding...")
embeddings = model.encode(texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True)

# quantize [-1,1] float -> int8
int8 = np.clip(np.round(embeddings * 127), -128, 127).astype(np.int8)
print(f"embeddings shape: {int8.shape}, bytes: {int8.nbytes}")

with open("embeddings.bin", "wb") as f:
    f.write(int8.tobytes())
print("Wrote embeddings.bin")
