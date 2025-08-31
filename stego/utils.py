def to_bin(data):
    if isinstance(data, str):
        return ''.join(format(ord(c), '08b') for c in data)
    elif isinstance(data, bytes):
        return ''.join(format(byte, '08b') for byte in data)
    elif isinstance(data, int):
        return format(data, '08b')
    else:
        raise TypeError("Type not supported")
    
def from_bin(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(c, 2)) for c in chars])