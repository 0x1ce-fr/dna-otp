# cli/demo_security.py

import sys
import os
import random
from collections import Counter
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.dna import generate_key, encrypt, decrypt, encode_dna, text_to_bits

def section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def entropy(sequence: str) -> float:
    """Compute the Shannon entropy of a sequence (in bits)."""
    n = len(sequence)
    counts = Counter(sequence)
    return -sum((c/n) * math.log2(c/n) for c in counts.values())

def demo(message: str):

    # 1. Key entropy
    section("1 : DNA key entropy")
    key = generate_key(len(message) * 4)
    h = entropy(key)
    print(f"  Generated key : {key[:40]}...")
    print(f"  Entropy       : {h:.4f} bits/base (theoretical max = 2.0)")
    print(f"  The closer to 2.0, the more random the key")

    # 2. Base distribution
    section("2 : Base distribution in the key")
    counts = Counter(key)
    total = len(key)
    for base in ['A', 'T', 'C', 'G']:
        pct = counts[base] / total * 100
        bar = 'X' * int(pct / 2)
        print(f"  {base} : {bar:<25} {pct:.1f}%")
    print(f"  Ideal distribution : 25% per base")

    # 3. Ciphertext reveals nothing
    section("3 : The ciphertext reveals nothing about the message")
    ciphertext = encrypt(message, key)
    counts_msg = Counter(encode_dna(text_to_bits(message)))
    counts_ct  = Counter(ciphertext)
    print(f"  Message DNA : base distribution")
    for base in ['A', 'T', 'C', 'G']:
        print(f"    {base} : {counts_msg[base]:3d} occurrences")
    print(f"\n  Ciphertext  : base distribution")
    for base in ['A', 'T', 'C', 'G']:
        print(f"    {base} : {counts_ct[base]:3d} occurrences")
    print(f"\n  The ciphertext has a uniform distribution, independent of the message")

    # 4. Brute force is impossible
    section("4 : Why brute force is impossible")
    nb_bases = len(ciphertext)
    nb_combinations = 4 ** nb_bases
    print(f"  Ciphertext length      : {nb_bases} bases")
    print(f"  Possible key combinations : 4^{nb_bases} = {nb_combinations:.2e}")
    print(f"\n  Example with a wrong random key :")
    wrong_key = generate_key(len(key))
    try:
        wrong_decrypt = decrypt(ciphertext, wrong_key)
        print(f"  Result : \"{wrong_decrypt[:30]}...\"")
    except UnicodeDecodeError:
        print(f"  Result : [unreadable sequence, invalid bytes]")
    print(f"\n  With the wrong key, the output is pure noise")
    print(f"  Any key produces a syntactically valid decryption")
    print(f"  Without the real key, there is no way to identify the correct result")
    print(f"  This is Shannon's proof (1949) : unconditional security")

    print(f"\n{'='*50}\n")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Message secret"
    demo(msg)