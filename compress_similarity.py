import pickle
import gzip

# Load original similarity matrix
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# Compress and save
with gzip.open("similarity_compressed.pkl.gz", "wb") as f:
    pickle.dump(similarity, f)

print("Compression completed!")