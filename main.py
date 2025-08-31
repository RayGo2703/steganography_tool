import argparse
from stego.image_stego import hide_text_in_image, extract_text_from_image
from stego.audio_stego import hide_text_in_audio, extract_text_from_audio

def main():
    parser = argparse.ArgumentParser(description="Steganography Tool")
    parser.add_argument("mode", choices=["hide", "extract"], help="Mode: hide or extract")
    parser.add_argument("type", choices=["image", "audio"], help="File type: image/audio")
    parser.add_argument("input", help="Input file")
    parser.add_argument("output", help="Output file (for hide mode)")
    parser.add_argument("--msg", help="Message to hide")
    parser.add_argument("--pwd", help="Password for encryption/decryption")

    args = parser.parse_args()

    if args.mode == "hide":
        if args.type == "image":
            hide_text_in_image(args.input, args.output, args.msg, args.pwd)
        elif args.type == "audio":
            hide_text_in_audio(args.input, args.output, args.msg, args.pwd)

    elif args.mode == "extract":
        if args.type == "image":
            print("Extracted:", extract_text_from_image(args.input, args.pwd))
        elif args.type == "audio":
            print("Extracted:", extract_text_from_audio(args.input, args.pwd))

if __name__ == "__main__":
    main()
