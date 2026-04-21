# cli/visualize.py

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.dna import text_to_bits, encode_dna, generate_key, decode_dna, xor_sequences, encrypt, decrypt

def step(n, title):
    print(f"\n{'_'*50}")
    print(f"  Step {n} : {title}")
    print(f"{'_'*50}")

def visualize(message: str):
    print(f"\n{'='*50}")
    print(f"  DNA-OTP : pipeline walkthrough")
    print(f"  Message : \"{message}\"")
    print(f"{'='*50}")

    # Step 1 : Text to bits
    step(1, "Text to bits")
    bits = text_to_bits(message)
    for i, char in enumerate(message):
        char_bits = f'{ord(char):08b}'
        print(f"  '{char}' ({ord(char):3d}) -> {char_bits}")
    print(f"\n  Full result : {bits[:48]}{'...' if len(bits) > 48 else ''}")

    # Step 2 : Bits to DNA
    step(2, "Bits to DNA sequence")
    dna_message = encode_dna(bits)
    print(f"  Mapping : 00->A  01->T  10->C  11->G")
    print(f"\n  First bits    : {bits[:12]}  ->  {dna_message[:6]}")
    print(f"  DNA sequence  : {dna_message[:40]}{'...' if len(dna_message) > 40 else ''}")

    # Step 3 : Key generation
    step(3, "DNA key generation (OTP)")
    key = generate_key(len(dna_message))
    print(f"  Length      : {len(key)} bases (= message length)")
    print(f"  Generated   : {key[:40]}{'...' if len(key) > 40 else ''}")
    print(f"  Each base is drawn randomly from A, T, C, G")

    # Step 4 : XOR encryption
    step(4, "Encryption by XOR")
    ciphertext = encrypt(message, key)
    print(f"  Message DNA : {dna_message[:20]}...")
    print(f"  DNA key     : {key[:20]}...")
    print(f"  {'_'*31}")
    print(f"  Ciphertext  : {ciphertext[:20]}...")
    print(f"\n  Bitwise XOR applied on binary representations")

    # Step 5 : Decryption
    step(5, "Decryption (XOR with the same key)")
    decrypted = decrypt(ciphertext, key)
    print(f"  Ciphertext  : {ciphertext[:20]}...")
    print(f"  DNA key     : {key[:20]}...")
    print(f"  {'_'*31}")
    print(f"  Decrypted   : \"{decrypted}\"")
    print(f"\n  Message recovered : {decrypted == message}")

    print(f"\n{'='*50}\n")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Hello DNA"
    visualize(msg)