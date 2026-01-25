from reedsolo import RSCodec
rsc = RSCodec(10)

def encode_chunk(chunk):
    return rsc.encode(chunk)

def decode_chunk(chunk):
    return rsc.decode(chunk)[0]
