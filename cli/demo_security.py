# cli/demo_security.py

import sys
import math
from collections import Counter

from core.dna import (
    generate_key,
    encrypt,
    decrypt,
    encode_dna,
    text_to_bits,
    purine_parity_digitize,
)


def section(title: str) -> None:
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")


def entropy(sequence: str) -> float:
    """Compute Shannon entropy of a sequence (bits per symbol)."""
    n = len(sequence)
    counts = Counter(sequence)
    return -sum((c/n) * math.log2(c/n) for c in counts.values())


def flip_base(base: str) -> str:
    """Flip a DNA base to a different one -- simulates a bit flip attack."""
    cycle = {'A': 'T', 'T': 'C', 'C': 'G', 'G': 'A'}
    return cycle[base]


def demo(message: str) -> None:

    # 1. Key entropy
    section("1 : DNA key entropy (os.urandom)")
    key = generate_key(len(message.encode('utf-8')) * 4)
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
    # 5PPD is only meaningful for physically synthesized DNA sequences.
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
        safe_output = wrong_decrypt[:30].encode('ascii', errors='replace').decode('ascii')
        print(f"  Result : \"{safe_output}...\"")
    except (UnicodeDecodeError, ValueError):
        print(f"  Result : [unreadable sequence, invalid bytes]")
    print(f"\n  With the wrong key, the output is pure noise")
    print(f"  Any key produces a syntactically plausible decryption")
    print(f"  Without the real key, there is no way to identify the correct result")
    print(f"  This is Shannon's proof (1949) : unconditional security")

    # 6. OTP does NOT guarantee integrity -- concrete attack demo
    section("6 : OTP has no integrity guarantee -- bit flip attack")
    print(f"  OTP guarantees confidentiality, not integrity.")
    print(f"  An attacker who flips a bit in the ciphertext in transit")
    print(f"  produces a corrupted plaintext -- with no error raised.\n")
    print(f"  Original ciphertext : {ciphertext[:20]}...")

    tampered = flip_base(ciphertext[0]) + ciphertext[1:]
    print(f"  Tampered ciphertext : {tampered[:20]}...")
    print(f"  (first base flipped : {ciphertext[0]} -> {tampered[0]})\n")

    try:
        tampered_decrypt = decrypt(tampered, key)
        print(f"  Decrypted tampered  : \"{tampered_decrypt}\"")
        print(f"  Original message    : \"{message}\"")
        print(f"\n  The receiver gets a wrong message with no warning.")
    except (UnicodeDecodeError, ValueError):
        print(f"  Decrypted tampered  : [invalid UTF-8 -- corruption detected by chance]")

    print(f"\n  In physical DNA-OTP, UMI copy-number statistics detect this.")
    print(f"  In software OTP, an HMAC layer would be required.")

    print(f"\n{'='*55}\n")


if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Secret message"
    demo(msg)