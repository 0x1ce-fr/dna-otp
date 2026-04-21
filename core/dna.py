# core/dna.py

import os
from collections import Counter

# Direct binary to DNA mapping (used for message encoding only)
BIN_TO_DNA = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}
DNA_TO_BIN = {v: k for k, v in BIN_TO_DNA.items()}

# Purines (A, G) vs Pyrimidines (C, T) — used for 5PPD
PURINES = {'A', 'G'}

def text_to_bits(text: str) -> str:
    """Convert a text string into a binary bit string."""
    return ''.join(f'{byte:08b}' for byte in text.encode('utf-8'))

def bits_to_text(bits: str) -> str:
    """Convert a binary bit string back into a text string."""
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return bytes(int(c, 2) for c in chars).decode('utf-8')

def encode_dna(bits: str) -> str:
    """Encode a bit string into a DNA sequence (2 bits per base)."""
    if len(bits) % 2 != 0:
        bits += '0'
    return ''.join(BIN_TO_DNA[bits[i:i+2]] for i in range(0, len(bits), 2))

def decode_dna(sequence: str) -> str:
    """Decode a DNA sequence back into a bit string."""
    return ''.join(DNA_TO_BIN[base] for base in sequence)

def generate_key(length_bases: int) -> str:
    """
    Generate a cryptographically secure random DNA key using os.urandom().

    os.urandom() draws entropy from the OS (hardware sources: CPU timing,
    hardware interrupts, etc.) unlike random.choice() which is a deterministic
    PRNG seeded from the clock. This is the recommended source for cryptographic
    applications in Python (see: PEP 506, secrets module).

    Each pair of random bits maps to one DNA base:
        00 -> A, 01 -> T, 10 -> C, 11 -> G
    """
    bases = []
    # Each byte from os.urandom() gives us 4 bases (2 bits each)
    n_bytes = (length_bases + 3) // 4
    raw = os.urandom(n_bytes)
    for byte in raw:
        for shift in (6, 4, 2, 0):
            two_bits = (byte >> shift) & 0b11
            bases.append(['A', 'T', 'C', 'G'][two_bits])
    return ''.join(bases[:length_bases])

def purine_parity_digitize(sequence: str, block_size: int = 5) -> str:
    """
    Block-5 Purine Parity Digitization (5PPD) as described in the CNRS paper.

    For each block of `block_size` bases, count the number of purines (A or G)
    modulo 2. This produces one bit per block.

    Why 5PPD instead of direct encoding?
    Direct encoding (00=A, 01=T...) is sensitive to synthesis biases: if A
    appears more often than G during chemical synthesis, the resulting bits
    are not uniformly distributed. 5PPD averages over positional biases and
    short-range correlations along the polymer chain, producing bits that
    pass NIST SP 800-90B entropy requirements (as demonstrated in the paper).
    """
    bits = []
    for i in range(0, len(sequence) - block_size + 1, block_size):
        block = sequence[i:i + block_size]
        purine_count = sum(1 for base in block if base in PURINES)
        bits.append(str(purine_count % 2))
    return ''.join(bits)

def xor_bits(bits1: str, bits2: str) -> str:
    """XOR two bit strings of equal length."""
    return ''.join(str(int(a) ^ int(b)) for a, b in zip(bits1, bits2))

def xor_sequences(seq1: str, seq2: str) -> str:
    """Perform a bitwise XOR on two DNA sequences via their binary representations."""
    bits1 = decode_dna(seq1)
    bits2 = decode_dna(seq2)
    xored = xor_bits(bits1, bits2)
    return encode_dna(xored)

def encrypt(message: str, key: str) -> str:
    """Encrypt a message using a DNA key (OTP)."""
    bits = text_to_bits(message)
    dna_message = encode_dna(bits)
    assert len(key) >= len(dna_message), "Key must be at least as long as the message."
    return xor_sequences(dna_message, key[:len(dna_message)])

def decrypt(ciphertext: str, key: str) -> str:
    """Decrypt a message using the same DNA key."""
    decrypted_dna = xor_sequences(ciphertext, key[:len(ciphertext)])
    bits = decode_dna(decrypted_dna)
    bits = bits[:len(bits) - len(bits) % 8]
    return bits_to_text(bits)