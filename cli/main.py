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
    print("  Ciphertext saved to cipher.dna")
    print("\n  WARNING: key.dna must be shared securely and deleted after use.")
    print("  Reusing the same key breaks OTP security.\n")

def cmd_decrypt(args):
    if not os.path.exists("key.dna"):
        print("\n  ERROR: key.dna not found. Has the key already been used?\n")
        sys.exit(1)
    if not os.path.exists("cipher.dna"):
        print("\n  ERROR: cipher.dna not found.\n")
        sys.exit(1)

    with open("key.dna", "r") as f:
        key = f.read()
    with open("cipher.dna", "r") as f:
        ciphertext = f.read()

    try:
        message = decrypt(ciphertext, key)
    except (ValueError, UnicodeDecodeError) as e:
        print(f"\n  ERROR: decryption failed -- {e}\n")
        sys.exit(1)

    print(f"\n{'='*50}")
    print(f"  Decrypted message : {message}")
    print(f"{'='*50}\n")

    # Enforce one-time use: delete the key after decryption
    os.remove("key.dna")
    print("  key.dna deleted -- OTP enforced, this key cannot be reused.\n")

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