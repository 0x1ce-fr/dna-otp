# DNA-OTP

Proof of concept of an encryption system inspired by synthetic DNA cryptography.

Based on the Franco-Japanese research published by the CNRS in 2026, which demonstrates that a synthetic DNA strand can serve as a One-Time Pad key, the only encryption system proven mathematically unbreakable (Shannon, 1949).

This project simulates the full pipeline in Python, without a lab.

---

## How it works

```
"Secret message"
      |
   Binary bits
      |
   DNA sequence (00->A, 01->T, 10->C, 11->G)
      |
   XOR with a random DNA key
      |
   TGAGCACGATCAGG...  (ciphertext)
```

The DNA key is generated randomly and used only once. This is the One-Time Pad principle. Without the key, the message is mathematically impossible to decrypt.

---

## Why it is unbreakable

### Shannon's proof (1949)

Shannon demonstrated that an encryption system is unconditionally secure if and only if three conditions are met:

1. **The key is as long as the message** — no repetition is possible
2. **The key is perfectly random** — each base A/T/C/G has exactly a 25% probability of appearing
3. **The key is used only once** — one-time pad

When these three conditions are met, the ciphertext contains no information about the original message. It is not "very hard to break" — it is mathematically proven impossible, regardless of the attacker's computing power.

### What the demo shows

```
Possible key combinations for 56 bases : 4^56 ~ 5.19 x 10^33
```

But brute force is not even the right attack vector. The real problem for an attacker is that any key produces a syntactically valid decryption. Without the real key, there is no way to identify the correct result among billions of false positives.

### The role of DNA

In the CNRS method, the key is not a file — it is a physical DNA strand. Only two copies exist: one held by the sender, one by the receiver. Any interception attempt leaves a detectable molecular trace. This is what makes the key exchange itself unbreakable — the fundamental problem that software-based One-Time Pad does not solve.

---

## Structure

```
dna_otp/
|-- core/
|   |-- dna.py              # Core logic: encoding, XOR, encryption
|-- cli/
|   |-- main.py             # Encryption and decryption tool
|   |-- visualize.py        # Step-by-step pipeline walkthrough
|   |-- demo_security.py    # Unbreakability demonstration
|-- README.md
```

---

## Usage

**Encrypt a message**
```bash
python cli/main.py encrypt "Secret message"
```

**Decrypt**
```bash
python cli/main.py decrypt
```

**Visualize the pipeline step by step**
```bash
python cli/visualize.py "Secret message"
```

**Demonstrate unbreakability**
```bash
python cli/demo_security.py "Secret message"
```

---

## References

- [CNRS - DNA cryptography (2026)](https://www.cnrs.fr/fr/presse/cryptographie-sur-adn-une-nouvelle-approche-franco-japonaise-fait-ses-preuves)
- Shannon, C. (1949). Communication Theory of Secrecy Systems

---

> Built for educational purposes only. Not intended for production use.