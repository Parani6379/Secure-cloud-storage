from modules.encryption import decrypt_data
from modules.erasure_coding import decode_chunk
from config import KEY

def reconstruct(chunks):
    data = []
    for c in chunks:
        decoded = decode_chunk(c)
        data.append(decrypt_data(decoded, KEY))
    return b''.join(data)
