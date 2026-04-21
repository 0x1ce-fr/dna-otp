# 🧬 DNA-OTP

Proof of concept d'un système de chiffrement inspiré de la cryptographie par ADN synthétique.

Basé sur les travaux franco-japonais publiés par le CNRS en 2026, qui démontrent qu'un brin d'ADN synthétique peut servir de clé One-Time Pad, le seul système de chiffrement prouvé mathématiquement inviolable (Shannon, 1949).

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

## Pourquoi c'est inviolable

### La preuve de Shannon (1949)

Shannon a démontré qu'un système de chiffrement est **inconditionnellement sûr** si et seulement si trois conditions sont réunies :

1. **La clé est aussi longue que le message** — pas de répétition possible
2. **La clé est parfaitement aléatoire** — chaque base A/T/C/G a exactement 25% de probabilité d'apparaître
3. **La clé n'est utilisée qu'une seule fois** — one-time pad

Quand ces trois conditions sont réunies, le chiffré ne contient **aucune information** sur le message original. Ce n'est pas "très difficile à casser" — c'est mathématiquement prouvé impossible, quelle que soit la puissance de calcul de l'adversaire.

### Ce que montre la démo

```
Combinaisons de clés possibles pour 56 bases : 4^56 ≈ 5.19 × 10³³
```

Mais le brute force n'est même pas le bon angle d'attaque. Le vrai problème pour un attaquant : **n'importe quelle clé produit un déchiffrement syntaxiquement valide**. Sans la vraie clé, impossible de distinguer le bon résultat des milliards de faux positifs.

### Le rôle de l'ADN

Dans la méthode du CNRS, la clé n'est pas un fichier — c'est un **brin d'ADN physique**. Il n'en existe que deux copies : une chez l'expéditeur, une chez le destinataire. Toute tentative d'interception laisse une trace moléculaire détectable. C'est ce qui rend l'échange de clé lui-même inviolable — le problème fondamental que le One-Time Pad logiciel ne résout pas.

---

## Structure

```
dna_otp/
├── core/
│   └── dna.py              # Logique : encodage, XOR, chiffrement
├── cli/
│   ├── main.py             # Outil de chiffrement/déchiffrement
│   ├── visualize.py        # Visualisation pédagogique du pipeline
│   └── demo_security.py    # Démonstration de l'inviolabilité
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

**Démontrer l'inviolabilité**
```bash
python cli/demo_security.py "Message secret"
```

---

## Références

- [CNRS — Cryptographie sur ADN (2026)](https://www.cnrs.fr/fr/presse/cryptographie-sur-adn-une-nouvelle-approche-franco-japonaise-fait-ses-preuves)
- Shannon, C. (1949). *Communication Theory of Secrecy Systems*

---

> Projet réalisé à des fins éducatives. Aucune utilisation en production.