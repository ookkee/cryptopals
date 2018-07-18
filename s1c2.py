import argparse

def xor(*args):
    """XOR arguments with each other.
    """
    if len(args) < 2:
        print("Need minimum 2 arguments")
        return

    result = int.from_bytes(args[0], byteorder="big")
    
    for arg in args[1:]:
        result = result ^ int.from_bytes(arg, byteorder="big")

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XOR arguments")
    parser.add_argument("inp", metavar="B", type=str, nargs="+",
        help="Bytes to XOR")
    parser.add_argument("--hex", dest="hex_input", action="store_true",
        help="Interpret input as hexadecimal")
    parser.set_defaults(hex_input=False)
    args = parser.parse_args()
    bts = list()
    for b in args.inp:
        if args.hex_input:
            import binascii
            bts.append(binascii.unhexlify(b))
        else:
            bts.append(b.encode("utf8"))
    print(hex(xor(*bts)))
