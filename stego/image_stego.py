from PIL import Image
from stego.crypto import encrypt_message, decrypt_message
from stego.utils import to_bin, from_bin

# End marker in binary to indicate end of hidden message
END_MARKER = "1111111111111110"

def hide_text_in_image(input_image, output_image, message, password=None):
    img = Image.open(input_image)
    if img.mode != 'RGB':
        img = img.convert("RGB")

    # Encrypt message if password is provided
    if password:
        message = encrypt_message(message, password)

    # Convert message to binary and append end marker
    binary_message = to_bin(message) + END_MARKER

    pixels = img.getdata()
    new_pixels = []
    msg_index = 0

    for pixel in pixels:
        r, g, b = pixel
        if msg_index < len(binary_message):
            r = (r & ~1) | int(binary_message[msg_index])
            msg_index += 1
        if msg_index < len(binary_message):
            g = (g & ~1) | int(binary_message[msg_index])
            msg_index += 1
        if msg_index < len(binary_message):
            b = (b & ~1) | int(binary_message[msg_index])
            msg_index += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(output_image)
    print(f"[+] Message hidden in {output_image}")


def extract_text_from_image(stego_image, password=None):
    img = Image.open(stego_image)
    pixels = img.getdata()
    binary_data = ""

    # Extract LSBs
    for pixel in pixels:
        for channel in pixel[:3]:
            binary_data += str(channel & 1)

    # Stop at end marker
    if END_MARKER in binary_data:
        binary_data = binary_data[:binary_data.index(END_MARKER)]

    # Convert binary to text
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = "".join([chr(int(byte, 2)) for byte in all_bytes if len(byte) == 8])

    # Decrypt if password provided
    if password:
        message = decrypt_message(message, password)

    return message
