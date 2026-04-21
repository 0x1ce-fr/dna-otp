# core/dna.py

import os
import random

# Mapping binaire <-> bases ADN
BIN_TO_DNA = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}
DNA_TO_BIN = {v: k for k, v in BIN_TO_DNA.items()}

def text_to_bits(text: str) -> str:
    """Convertit un texte en chaîne de bits."""
    return ''.join(f'{byte:08b}' for byte in text.encode('utf-8'))

def bits_to_text(bits: str) -> str:
    """Reconvertit une chaîne de bits en texte."""
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return bytes(int(c, 2) for c in chars).decode('utf-8')

def encode_dna(bits: str) -> str:
    """Encode une chaîne de bits en séquence ADN (2 bits par base)."""
    # On padde si nécessaire pour avoir un multiple de 2
    if len(bits) % 2 != 0:
        bits += '0'
    return ''.join(BIN_TO_DNA[bits[i:i+2]] for i in range(0, len(bits), 2))

def decode_dna(sequence: str) -> str:
    """Décode une séquence ADN en bits."""
    return ''.join(DNA_TO_BIN[base] for base in sequence)

def generate_key(length_bases: int) -> str:
    """Génère une clé ADN aléatoire (OTP) de la longueur donnée."""
    bases = ['A', 'T', 'C', 'G']
    return ''.join(random.choice(bases) for _ in range(length_bases))

def xor_sequences(seq1: str, seq2: str) -> str:
    """XOR bit-à-bit de deux séquences ADN (via leurs représentations binaires)."""
    bits1 = decode_dna(seq1)
    bits2 = decode_dna(seq2)
    xored = ''.join(str(int(a) ^ int(b)) for a, b in zip(bits1, bits2))
    return encode_dna(xored)

def encrypt(message: str, key: str) -> str:
    """Chiffre un message avec une clé ADN (OTP)."""
    bits = text_to_bits(message)
    dna_message = encode_dna(bits)
    assert len(key) >= len(dna_message), "La clé doit être au moins aussi longue que le message."
    return xor_sequences(dna_message, key[:len(dna_message)])

def decrypt(ciphertext: str, key: str) -> str:
    """Déchiffre un message avec la même clé ADN."""
    decrypted_dna = xor_sequences(ciphertext, key[:len(ciphertext)])
    bits = decode_dna(decrypted_dna)
    # On retire le padding éventuel
    bits = bits[:len(bits) - len(bits) % 8]
    return bits_to_text(bits)