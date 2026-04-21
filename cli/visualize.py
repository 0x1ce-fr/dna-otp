# cli/visualize.py

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.dna import text_to_bits, encode_dna, generate_key, decode_dna, xor_sequences, encrypt, decrypt

def step(n, title):
    print(f"\n{'─'*50}")
    print(f"  Étape {n} — {title}")
    print(f"{'─'*50}")

def visualize(message: str):
    print(f"\n{'='*50}")
    print(f"  DNA-OTP : visualisation du pipeline")
    print(f"  Message : \"{message}\"")
    print(f"{'='*50}")

    # Étape 1 — Texte → Bits
    step(1, "Texte → Bits")
    bits = text_to_bits(message)
    for i, char in enumerate(message):
        char_bits = f'{ord(char):08b}'
        print(f"  '{char}' ({ord(char):3d}) → {char_bits}")
    print(f"\n  Résultat complet : {bits[:48]}{'...' if len(bits) > 48 else ''}")

    # Étape 2 — Bits → ADN
    step(2, "Bits → Séquence ADN")
    dna_message = encode_dna(bits)
    print(f"  Règle : 00→A  01→T  10→C  11→G")
    print(f"\  Premiers bits : {bits[:12]}  →  {dna_message[:6]}")
    print(f"  Séquence ADN  : {dna_message[:40]}{'...' if len(dna_message) > 40 else ''}")

    # Étape 3 — Génération clé
    step(3, "Génération de la clé ADN (OTP)")
    key = generate_key(len(dna_message))
    print(f"  Longueur       : {len(key)} bases (= longueur du message)")
    print(f"  Clé générée    : {key[:40]}{'...' if len(key) > 40 else ''}")
    print(f"  → Chaque base est tirée aléatoirement parmi A, T, C, G")

    # Étape 4 — XOR
    step(4, "Chiffrement par XOR")
    ciphertext = encrypt(message, key)
    print(f"  Message ADN : {dna_message[:20]}...")
    print(f"  Clé ADN     : {key[:20]}...")
    print(f"  ─────────────────────────────")
    print(f"  Chiffré     : {ciphertext[:20]}...")
    print(f"\n  → XOR bit à bit sur les représentations binaires")

    # Étape 5 — Déchiffrement
    step(5, "Déchiffrement (XOR avec la même clé)")
    decrypted = decrypt(ciphertext, key)
    print(f"  Chiffré     : {ciphertext[:20]}...")
    print(f"  Clé ADN     : {key[:20]}...")
    print(f"  ─────────────────────────────")
    print(f"  Déchiffré   : \"{decrypted}\"")
    print(f"\n  ✓ Message retrouvé : {decrypted == message}")

    print(f"\n{'='*50}\n")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Hello ADN"
    visualize(msg)