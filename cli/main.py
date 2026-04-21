# cli/main.py

import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.dna import generate_key, encrypt, decrypt

def cmd_encrypt(args):
    key = generate_key(len(args.message) * 4)  # 4 bases par caractère (8 bits / 2)
    ciphertext = encrypt(args.message, key)
    
    print(f"\n{'='*50}")
    print(f"  Message original : {args.message}")
    print(f"  Clé ADN          : {key[:40]}...")
    print(f"  Message chiffré  : {ciphertext[:40]}...")
    print(f"{'='*50}\n")
    
    # Sauvegarde clé + chiffré pour pouvoir déchiffrer ensuite
    with open("key.dna", "w") as f:
        f.write(key)
    with open("cipher.dna", "w") as f:
        f.write(ciphertext)
    
    print("  Clé sauvegardée dans key.dna")
    print("  Message chiffré sauvegardé dans cipher.dna\n")

def cmd_decrypt(args):
    with open("key.dna", "r") as f:
        key = f.read()
    with open("cipher.dna", "r") as f:
        ciphertext = f.read()
    
    message = decrypt(ciphertext, key)
    
    print(f"\n{'='*50}")
    print(f"  Message déchiffré : {message}")
    print(f"{'='*50}\n")

def main():
    parser = argparse.ArgumentParser(
        description="DNA-OTP : chiffrement par séquence ADN synthétique"
    )
    subparsers = parser.add_subparsers(dest="command")

    enc = subparsers.add_parser("encrypt", help="Chiffrer un message")
    enc.add_argument("message", type=str, help="Message à chiffrer")

    subparsers.add_parser("decrypt", help="Déchiffrer le dernier message")

    args = parser.parse_args()

    if args.command == "encrypt":
        cmd_encrypt(args)
    elif args.command == "decrypt":
        cmd_decrypt(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()