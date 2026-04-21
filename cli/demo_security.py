# cli/demo_security.py

import sys
import os
import math
from collections import Counter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.dna import generate_key, encrypt, decrypt, encode_dna, text_to_bits, purine_parity_digitize

def section(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")

def entropy(sequence: str) -> float:
    """Compute Shannon entropy of a sequence (bits per symbol)."""
    n = len(sequence)
    counts = Counter(sequence)
    return -sum((c/n) * math.log2(c/n) for c in counts.values())

def demo(message: str):

    # 1. Key entropy
    section("1 : DNA key entropy (os.urandom)")
    key = generate_key(len(message) * 4)
    h = entropy(key)
    print(f"  Generated key : {key[:40]}...")
    print(f"  Entropy       : {h:.4f} bits/base (theoretical max = 2.0)")
    print(f"  Source        : os.urandom() -- OS hardware entropy pool")
    print(f"  NOT random.choice() -- that is a deterministic PRNG")

    # 2. Base distribution
    section("2 : Base distribution in the key")
    counts = Counter(key)
    total = len(key)
    for base in ['A', 'T', 'C', 'G']:
        pct = counts[base] / total * 100
        bar = 'X' * int(pct / 2)
        print(f"  {base} : {bar:<25} {pct:.1f}%")
    print(f"  Ideal distribution : 25% per base")

    # 3. 5PPD demonstration
    # Note: pedagogical demonstration only.
    # The key here comes from os.urandom() and has no synthesis bias.
    # 5PPD is only meaningful for physically synthesized DNA sequences,
    # where chemical processes introduce positional biases and correlations.
    section("3 : Block-5 Purine Parity Digitization (5PPD)")
    print(f"  Note: pedagogical demonstration of the CNRS method.")
    print(f"  5PPD corrects synthesis biases in physical DNA -- not applicable")
    print(f"  to os.urandom() keys which are already uniformly distributed.\n")
    sample_seq = generate_key(50)
    print(f"  Sample DNA sequence : {sample_seq}")
    print(f"\n  Purines = A or G, Pyrimidines = C or T")
    print(f"  For each block of 5 bases, count purines modulo 2:\n")
    for i in range(0, 25, 5):
        block = sample_seq[i:i+5]
        purine_count = sum(1 for b in block if b in {'A', 'G'})
        bit = purine_count % 2
        print(f"  Block {i//5 + 1}: {block}  purines={purine_count}  bit={bit}")
    bits_5ppd = purine_parity_digitize(sample_seq)
    print(f"\n  5PPD output : {bits_5ppd}")
    print(f"  Entropy of 5PPD bits : {entropy(bits_5ppd):.4f} bits/symbol")
    print(f"\n  In real DNA synthesis, this removes positional biases and")
    print(f"  short-range correlations along the polymer chain.")
    print(f"  The CNRS experiment measured H_min ~ 0.96 bits/bit after 5PPD.")

    # 4. Ciphertext reveals nothing
    section("4 : The ciphertext reveals nothing about the message")
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

    # 5. Brute force is impossible
    section("5 : Why brute force is impossible")
    nb_bases = len(ciphertext)
    nb_combinations = 4 ** nb_bases
    print(f"  Ciphertext length         : {nb_bases} bases")
    print(f"  Possible key combinations : 4^{nb_bases} = {nb_combinations:.2e}")
    print(f"\n  Example with a wrong random key :")
    wrong_key = generate_key(len(key))
    try:
        wrong_decrypt = decrypt(ciphertext, wrong_key)
        # Safely truncate and encode before printing to avoid terminal encoding errors
        safe_output = wrong_decrypt[:30].encode('ascii', errors='replace').decode('ascii')
        print(f"  Result : \"{safe_output}...\"")
    except (UnicodeDecodeError, ValueError):
        print(f"  Result : [unreadable sequence, invalid bytes]")
    print(f"\n  With the wrong key, the output is pure noise")
    print(f"  Any key produces a syntactically plausible decryption")
    print(f"  Without the real key, there is no way to identify the correct result")
    print(f"  This is Shannon's proof (1949) : unconditional security")

    # 6. What OTP does NOT guarantee
    section("6 : What OTP does NOT guarantee")
    print(f"  OTP provides confidentiality, not integrity.")
    print(f"  An attacker who flips bits in the ciphertext in transit")
    print(f"  produces a different plaintext -- undetected by the receiver.")
    print(f"  In physical DNA-OTP, UMI tagging detects such interference.")
    print(f"  In this software simulation, there is no integrity check.")

    print(f"\n{'='*55}\n")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Secret message"
    demo(msg)