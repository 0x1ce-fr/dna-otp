# DNA-OTP

> Proof of concept of an encryption system inspired by synthetic DNA cryptography.
> Based on CNRS. (2026) HAL-05560338 CC BY 4.0

---

## The problem : secure key distribution

Every modern encryption system (AES, RSA...) relies on **computational security** : it is hard to break,
but not impossible. Given enough computing power, any key can eventually be cracked.

The One-Time Pad (OTP), proven by Shannon in 1949, is the only system offering **unconditional security** :
it is mathematically impossible to break, regardless of the attacker's computing power.

The catch : the key must be as long as the message, perfectly random, and used only once.
Distributing such keys securely over long distances has been the fundamental unsolved problem until now.

---

## Shannon's proof

A cryptosystem offers **perfect secrecy** if and only if :

$$P(M = m \mid C = c) = P(M = m)$$

Observing the ciphertext $c$ gives zero information about the plaintext $m$.
Shannon (1949) proved this holds if and only if three conditions are simultaneously met :

$$|K| \geq |M| \qquad H(K) = \log_2|K| \qquad K \text{ used only once}$$

Where :
- $|K|$ is the key length, $|M|$ is the message length
- $H(K) = -\sum_{k} P(k) \log_2 P(k)$ is the entropy of the key (Shannon entropy)
- $H(K) = \log_2|K|$ means the key is **perfectly uniform** every possible key is equally likely

For a DNA key of $n$ bases over alphabet $\{A, T, C, G\}$ :

$$H(K) = n \cdot \log_2 4 = 2n \text{ bits}$$

The number of possible keys is $4^n$. For $n = 56$ bases (a 14-character message) :

$$4^{56} \approx 5.19 \times 10^{33} \text{ possible keys}$$

Brute force is not even the right attack. Every key produces a valid-looking decryption.
Without the real key, there is no way to identify the correct plaintext.

---

## The XOR operation

Encryption and decryption both use the same operation : **bitwise XOR** ($\oplus$).

| $a$ | $b$ | $a \oplus b$ |
|-----|-----|--------------|
|  0  |  0  |      0       |
|  0  |  1  |      1       |
|  1  |  0  |      1       |
|  1  |  1  |      0       |

The key property : XOR is its own inverse.

$$(M \oplus K) \oplus K = M$$

So encryption and decryption are the same operation :

$$C = M \oplus K \qquad M = C \oplus K$$

Applied to DNA sequences, the XOR operates on the binary representations of each base.

---

## The pipeline

```
Alice                                          Bob
  |                                              |
  |   "Secret"  -->  01010011 01100101 ...       |
  |                       |                      |
  |              DNA encoding (2 bits/base)      |
  |              00->A  01->T  10->C  11->G      |
  |                       |                      |
  |              TACCGTAC...  (message in DNA)   |
  |                       |                      |
  |   os.urandom()        |                      |
  |   GCTAGTCA...  (key)  |                      |
  |           \           |                      |
  |            XOR (bitwise, base by base)       |
  |                       |                      |
  |              ATCGTGAC...  (ciphertext)       |
  |                       |                      |
  | -------- public channel ------------------>  |
  |                       |                      |
  |                  same key (shared)           |
  |                       |                      |
  |                  XOR again                   |
  |                       |                      |
  |              TACCGTAC...  (recovered DNA)    |
  |                       |                      |
  |              DNA decoding                    |
  |                       |                      |
  |              "Secret"  <--  01010011 ...     |
```

---

## Block-5 Purine Parity Digitization (5PPD)

Direct base encoding (00=A, 01=T...) is sensitive to synthesis biases.
During chemical DNA synthesis, bases are not incorporated with equal probability at every position.

The CNRS paper introduces **5PPD** : for each block of 5 bases, count the number of purines
($A$ or $G$) modulo 2. This produces one unbiased bit per block.

$$b_i = \left( \sum_{j=1}^{5} \mathbb{1}[\text{base}_j \in \{A, G\}] \right) \mod 2$$

Example :

```
DNA block :  A  C  A  T  G
Purine?   :  1  0  1  0  1   -> sum = 3
3 mod 2   :  1                -> bit = 1

DNA block :  T  T  C  C  A
Purine?   :  0  0  0  0  1   -> sum = 1
1 mod 2   :  1                -> bit = 1

DNA block :  G  C  T  A  C
Purine?   :  1  0  0  1  0   -> sum = 2
2 mod 2   :  0                -> bit = 0
```

Why does this work? Even if $A$ appears more often than $G$ at a given position,
the parity of the count over a block of 5 averages out positional biases
and short-range correlations along the polymer chain.

The CNRS experiment measured a min-entropy of $H_{\min} \approx 0.96$ bits/bit after 5PPD,
on par with NIST-approved cryptographic random number generators (FIPS 140-3).

---

## Key generation : os.urandom()

This project uses `os.urandom()` to generate the DNA key.

`os.urandom()` draws entropy from the OS hardware pool :
- CPU timing jitter
- Hardware interrupts
- Thermal noise (on supported hardware)

This is fundamentally different from `random.choice()`, which is a **deterministic PRNG**
seeded from the system clock. A PRNG is not suitable for cryptography.

```python
# Wrong -- deterministic, predictable
import random
key = ''.join(random.choice('ATCG') for _ in range(n))

# Right -- hardware entropy source
import os
raw = os.urandom(n_bytes)
# each byte -> 4 bases (2 bits each)
```

The entropy of a key of $n$ bases generated by `os.urandom()` :

$$H(K) \approx 2n \text{ bits} \qquad \text{(close to theoretical maximum)}$$

---

## Limitations

This is a software simulation. Several components differ from the real CNRS protocol :

**Key generation**
`os.urandom()` draws from the OS hardware entropy pool. This is cryptographically suitable
for software, but not equivalent to the physical randomness of synthetic DNA synthesis,
which arises from the stochastic incorporation of nucleotides during chemical reactions.

**Encoding**
Message encoding uses direct binary mapping (00=A, 01=T, 10=C, 11=G).
The CNRS paper shows this is biased for real DNA synthesis.
5PPD is implemented here for key binarization demonstration.

**No index-payload architecture**
The real protocol uses paired index and payload DNA strands.
Alice and Bob publicly exchange indices to synchronize, while keeping payloads secret.
This sifting stage (analogous to QKD) is not implemented here.

**No interception detection**
The paper demonstrates that attacks can be detected via Unique Molecular Identifier (UMI)
statistics. This requires physical DNA samples and nanopore sequencing.

---

## Structure

```
dna_otp/
|-- core/
|   |-- dna.py              # Core logic : encoding, XOR, 5PPD, encryption
|-- cli/
|   |-- main.py             # Encryption and decryption tool
|   |-- demo_security.py    # Unbreakability and 5PPD demonstration
|-- tests/
|   |-- test_dna.py         # Unit tests (26 tests)
|-- .github/
|   |-- workflows/
|       |-- tests.yml       # GitHub Actions CI
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

**Demonstrate unbreakability and 5PPD**
```bash
python cli/demo_security.py "Secret message"
```

**Run tests**
```bash
pytest tests/ -v
```

---

## References

- CNRS. (2026). *Synchronized DNA sources for unconditionally secure cryptography.*
  HAL-05560338. https://hal.science/hal-05560338v1 CC BY 4.0
- Shannon, C. (1949). *Communication Theory of Secrecy Systems.* Bell System Technical Journal, 28(4), 656-715.

---

> Built for educational purposes only. Not intended for production use.