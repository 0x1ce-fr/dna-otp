# core/dna.py

import os
import random
from collections import Counter

# Binary to DNA base mapping
BIN_TO_DNA = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}
DNA_TO_BIN = {v: k for k, v in BIN_TO_DNA.items()}

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
    """Generate a random DNA key (OTP) of the given length."""
    bases = ['A', 'T', 'C', 'G']
    return ''.join(random.choice(bases) for _ in range(length_bases))

def xor_sequences(seq1: str, seq2: str) -> str:
    """Perform a bitwise XOR on two DNA sequences."""
    bits1 = decode_dna(seq1)
    bits2 = decode_dna(seq2)
    xored = ''.join(str(int(a) ^ int(b)) for a, b in zip(bits1, bits2))
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