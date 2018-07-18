import argparse
import logging

def base64_encode(data):
    """Encodes data in base64.
    """
    b64charset = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    mask = int("111111", 2)

    inp = bytearray(data)

    logging.debug("Input:",inp)
    logging.debug("Input length:", len(inp))

    encoded = bytearray()

    # Ceiling division, we want to include the rest
    for i in range(-(-len(inp)//3)):
        # Get 3 bytes or less
        inp_slice = inp[(i*3):]
        if len(inp_slice) > 3:
            inp_slice = inp_slice[:3]

        # Convert to int for bitwise operations
        inp_bits = int.from_bytes(inp_slice, byteorder="big")
        
        # Pad for base 64 if needed
        if len(inp_slice) == 2:
            inp_bits = inp_bits << 2
        elif len(inp_slice) == 1:
            inp_bits = inp_bits << 4

        for j in reversed(range(len(inp_slice)+1)):
            encoded.append(b64charset[(inp_bits >> 6*j) & mask])

    # Add padding characters
    if len(encoded) % 4 == 3:
        encoded.append(61)
    elif len(encoded) % 4 == 2:
        encoded.append(61)
        encoded.append(61)

    logging.debug("b64 encoded:",encoded)

    return encoded

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode with base64")
    parser.add_argument("strings", metavar="S", type=str, nargs="+",
        help="Strings to encode")
    parser.add_argument("--hex", dest="hex_input", action="store_true",
        help="Interpret input as hexadecimal")
    parser.set_defaults(hex_input=False)
    args = parser.parse_args()
    for s in args.strings:
        if args.hex_input:
            import binascii
            inp = binascii.unhexlify(s)
            print(base64_encode(inp).decode())
        else:
            print(base64_encode(s.encode("utf8")).decode())
