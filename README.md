# 🧬 DNA-OTP

Proof of concept d'un système de chiffrement inspiré de la cryptographie par ADN synthétique.

Basé sur les travaux franco-japonais publiés par le CNRS en 2026, qui démontrent qu'un brin d'ADN synthétique peut servir de clé One-Time Pad, seul système de chiffrement prouvé mathématiquement inviolable (Shannon, 1949).

Ce projet simule l'intégralité du pipeline en Python, sans labo.

---

## Comment ça marche

```
"Message secret"
      ↓
   Bits binaires
      ↓
   Séquence ADN (00→A, 01→T, 10→C, 11→G)
      ↓
   XOR avec une clé ADN aléatoire
      ↓
   TGAGCACGATCAGG...  (chiffré)
```

La clé ADN est générée aléatoirement et utilisée une seule fois, c'est le principe du One-Time Pad. Sans la clé, le message est mathématiquement impossible à déchiffrer.

---

## Structure

```
dna_otp/
├── core/
│   └── dna.py          # Logique : encodage, XOR, chiffrement
├── cli/
│   ├── main.py         # Outil de chiffrement/déchiffrement
│   └── visualize.py    # Visualisation pédagogique du pipeline
└── README.md
```

---

## Utilisation

**Chiffrer un message**
```bash
python cli/main.py encrypt "Message secret"
```

**Déchiffrer**
```bash
python cli/main.py decrypt
```

**Visualiser le pipeline étape par étape**
```bash
python cli/visualize.py "Message secret"
```

---

## Références

- [CNRS — Cryptographie sur ADN (2026)](https://www.cnrs.fr/fr/presse/cryptographie-sur-adn-une-nouvelle-approche-franco-japonaise-fait-ses-preuves)
- Shannon, C. (1949). *Communication Theory of Secrecy Systems*

---

> Projet réalisé à des fins éducatives. Aucune utilisation en production.