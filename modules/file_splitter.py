from config import CHUNK_SIZE

def split_file(data):
    return [data[i:i+CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]
