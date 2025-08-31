import wave
import struct
from stego.crypto import encrypt_message, decrypt_message
from stego.utils import to_bin, from_bin

# Binary delimiter to mark the end of hidden data
END_MARKER = "1111111111111110"

def hide_text_in_audio(input_audio, output_audio, message, password=None):
    # Encrypt message if password provided
    if password:
        message = encrypt_message(message, password)

    # Convert message to binary + add end marker
    binary_message = to_bin(message) + END_MARKER
    msg_index = 0

    # Open the WAV file
    with wave.open(input_audio, "rb") as audio:
        params = audio.getparams()
        num_frames = audio.getnframes()
        raw_data = audio.readframes(num_frames)
        samples = list(struct.unpack("<" + "h" * (len(raw_data) // 2), raw_data))

    # Modify LSB of samples
    for i in range(len(samples)):
        if msg_index < len(binary_message):
            samples[i] = (samples[i] & ~1) | int(binary_message[msg_index])
            msg_index += 1
        else:
            break

    # Pack modified samples back into bytes
    new_data = struct.pack("<" + "h" * len(samples), *samples)

    # Write stego audio
    with wave.open(output_audio, "wb") as stego:
        stego.setparams(params)
        stego.writeframes(new_data)

    print(f"[+] Message hidden in {output_audio}")


def extract_text_from_audio(stego_audio, password=None):
    with wave.open(stego_audio, "rb") as audio:
        num_frames = audio.getnframes()
        raw_data = audio.readframes(num_frames)
        samples = list(struct.unpack("<" + "h" * (len(raw_data) // 2), raw_data))

    # Extract LSBs from samples
    binary_data = "".join([str(sample & 1) for sample in samples])

    # Stop when we see the END_MARKER
    end_index = binary_data.find(END_MARKER)
    if end_index != -1:
        binary_data = binary_data[:end_index]

    # Convert binary to text
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = "".join([chr(int(byte, 2)) for byte in all_bytes if len(byte) == 8])

    # Decrypt if needed
    if password:
        message = decrypt_message(message, password)

    return message
