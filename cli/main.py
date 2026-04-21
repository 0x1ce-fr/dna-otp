# cli/main.py

import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.dna import generate_key, encrypt, decrypt

def cmd_encrypt(args):
    key = generate_key(len(args.message) * 4)
    ciphertext = encrypt(args.message, key)

    print(f"\n{'='*50}")
    print(f"  Original message : {args.message}")
    print(f"  DNA key          : {key[:40]}...")
    print(f"  Encrypted        : {ciphertext[:40]}...")
    print(f"{'='*50}\n")

    with open("key.dna", "w") as f:
        f.write(key)
    with open("cipher.dna", "w") as f:
        f.write(ciphertext)

    print("  Key saved to key.dna")
    print("  Ciphertext saved to cipher.dna\n")

def cmd_decrypt(args):
    with open("key.dna", "r") as f:
        key = f.read()
    with open("cipher.dna", "r") as f:
        ciphertext = f.read()

    message = decrypt(ciphertext, key)

    print(f"\n{'='*50}")
    print(f"  Decrypted message : {message}")
    print(f"{'='*50}\n")

def main():
    parser = argparse.ArgumentParser(
        description="DNA-OTP: encryption using synthetic DNA sequences"
    )
    subparsers = parser.add_subparsers(dest="command")

    enc = subparsers.add_parser("encrypt", help="Encrypt a message")
    enc.add_argument("message", type=str, help="Message to encrypt")

    subparsers.add_parser("decrypt", help="Decrypt the last message")

    args = parser.parse_args()

    if args.command == "encrypt":
        cmd_encrypt(args)
    elif args.command == "decrypt":
        cmd_decrypt(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()