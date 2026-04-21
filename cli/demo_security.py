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

def entropie(sequence: str) -> float:
    """Calcule l'entropie de Shannon d'une séquence (en bits)."""
    n = len(sequence)
    counts = Counter(sequence)
    return -sum((c/n) * math.log2(c/n) for c in counts.values())

def demo(message: str):

    # ── 1. Entropie de la clé ──────────────────────────────
    section("1 — Entropie de la clé ADN")
    key = generate_key(len(message) * 4)
    h = entropie(key)
    print(f"  Clé générée : {key[:40]}...")
    print(f"  Entropie    : {h:.4f} bits/base (max théorique = 2.0)")
    print(f"  → Plus l'entropie est proche de 2.0, plus la clé est aléatoire")

    # ── 2. Distribution des bases ──────────────────────────
    section("2 — Distribution des bases dans la clé")
    counts = Counter(key)
    total = len(key)
    for base in ['A', 'T', 'C', 'G']:
        pct = counts[base] / total * 100
        bar = '█' * int(pct / 2)
        print(f"  {base} : {bar:<25} {pct:.1f}%")
    print(f"  → Distribution idéale : 25% par base")

    # ── 3. Le chiffré ne révèle rien ──────────────────────
    section("3 — Le chiffré ne révèle rien du message")
    ciphertext = encrypt(message, key)
    counts_msg = Counter(encode_dna(text_to_bits(message)))
    counts_ct  = Counter(ciphertext)
    print(f"  Message ADN — distribution des bases :")
    for base in ['A', 'T', 'C', 'G']:
        print(f"    {base} : {counts_msg[base]:3d} occurrences")
    print(f"\n  Chiffré     — distribution des bases :")
    for base in ['A', 'T', 'C', 'G']:
        print(f"    {base} : {counts_ct[base]:3d} occurrences")
    print(f"\n  → Le chiffré a une distribution uniforme, indépendante du message")

    # ── 4. Brute force : impossible ────────────────────────
    section("4 — Pourquoi le brute force est impossible")
    nb_bases = len(ciphertext)
    nb_combinaisons = 4 ** nb_bases
    print(f"  Longueur du chiffré : {nb_bases} bases")
    print(f"  Combinaisons de clés possibles : 4^{nb_bases} = {nb_combinaisons:.2e}")
    print(f"\n  Exemple — avec une mauvaise clé aléatoire :")
    fausse_cle = generate_key(len(key))
    try:
        faux_decrypt = decrypt(ciphertext, fausse_cle)
        print(f"  Résultat : \"{faux_decrypt[:30]}...\"")
    except UnicodeDecodeError:
        print(f"  Résultat : [séquence illisible — octets invalides]")
    print(f"\n  → Avec la mauvaise clé, le résultat est du bruit pur")
    print(f"\n  → N'importe quelle clé produit un 'déchiffrement' plausible")
    print(f"  → Sans la vraie clé, impossible de savoir lequel est le bon")
    print(f"  → C'est la preuve de Shannon (1949) : sécurité inconditionnelle")

    print(f"\n{'='*50}\n")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Message secret"
    demo(msg)