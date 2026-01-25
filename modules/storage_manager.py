import os

def store_chunks(base_path, chunks):
    nodes = [f"{base_path}/nodes/node{i}" for i in range(1,5)]
    for n in nodes:
        os.makedirs(n, exist_ok=True)

    for i, chunk in enumerate(chunks):
        node = nodes[i % 4]
        with open(f"{node}/chunk_{i}.bin", "wb") as f:
            f.write(chunk)

def load_chunks(base_path):
    chunks = []
    for i in range(1,5):
        node = f"{base_path}/nodes/node{i}"
        if os.path.exists(node):
            for file in sorted(os.listdir(node)):
                with open(f"{node}/{file}", "rb") as f:
                    chunks.append(f.read())
    return chunks
