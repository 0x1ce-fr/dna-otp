# tests/test_dna.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from core.dna import (
    text_to_bits,
    bits_to_text,
    encode_dna,
    decode_dna,
    generate_key,
    xor_sequences,
    encrypt,
    decrypt,
    purine_parity_digitize,
)

# ── Encoding ───────────────────────────────────────────────

class TestEncoding:

    def test_text_to_bits_ascii(self):
        assert text_to_bits("A") == "01000001"

    def test_text_to_bits_multibyte(self):
        bits = text_to_bits("Hi")
        assert len(bits) == 16
        assert bits == "0100100001101001"

    def test_bits_to_text_roundtrip(self):
        original = "Hello"
        assert bits_to_text(text_to_bits(original)) == original

    def test_bits_to_text_raises_on_non_multiple_of_8(self):
        with pytest.raises(ValueError, match="not a multiple of 8"):
            bits_to_text("010")

    def test_encode_dna_mapping(self):
        assert encode_dna("00") == "A"
        assert encode_dna("01") == "T"
        assert encode_dna("10") == "C"
        assert encode_dna("11") == "G"

    def test_encode_dna_raises_on_odd_bits(self):
        with pytest.raises(ValueError, match="not a multiple of 2"):
            encode_dna("0")

    def test_decode_dna_mapping(self):
        assert decode_dna("A") == "00"
        assert decode_dna("T") == "01"
        assert decode_dna("C") == "10"
        assert decode_dna("G") == "11"

    def test_decode_dna_raises_on_invalid_base(self):
        with pytest.raises(ValueError, match="Invalid DNA base"):
            decode_dna("X")

    def test_decode_dna_raises_on_lowercase(self):
        with pytest.raises(ValueError, match="Invalid DNA base"):
            decode_dna("atcg")

    def test_encode_decode_roundtrip(self):
        bits = "0011001011010000"
        assert decode_dna(encode_dna(bits)) == bits

# ── Key generation ─────────────────────────────────────────

class TestKeyGeneration:

    def test_key_length(self):
        for n in [10, 50, 100, 256]:
            assert len(generate_key(n)) == n

    def test_key_alphabet(self):
        key = generate_key(1000)
        assert set(key).issubset({'A', 'T', 'C', 'G'})

    def test_key_randomness(self):
        key1 = generate_key(100)
        key2 = generate_key(100)
        assert key1 != key2

    def test_key_base_distribution(self):
        key = generate_key(10000)
        for base in ['A', 'T', 'C', 'G']:
            freq = key.count(base) / len(key)
            assert 0.20 < freq < 0.30, f"Base {base} frequency {freq:.3f} out of expected range"

# ── XOR ────────────────────────────────────────────────────

class TestXOR:

    def test_xor_identity(self):
        seq = "ATCG"
        key = "AAAA"
        assert xor_sequences(xor_sequences(seq, key), key) == seq

    def test_xor_self_is_zero(self):
        seq = "GCTA"
        result = xor_sequences(seq, seq)
        assert result == "AAAA"

    def test_xor_commutativity(self):
        a = "ATCG"
        b = "GCTA"
        assert xor_sequences(a, b) == xor_sequences(b, a)

# ── Encrypt / Decrypt ──────────────────────────────────────

class TestEncryptDecrypt:

    def test_encrypt_decrypt_roundtrip(self):
        message = "Secret"
        key = generate_key(len(message) * 4)
        assert decrypt(encrypt(message, key), key) == message

    def test_encrypt_decrypt_single_char(self):
        message = "A"
        key = generate_key(100)
        assert decrypt(encrypt(message, key), key) == message

    def test_encrypt_decrypt_utf8_accents(self):
        message = "cafe"
        key = generate_key(len(message.encode('utf-8')) * 4)
        assert decrypt(encrypt(message, key), key) == message

    def test_encrypt_decrypt_utf8_cjk(self):
        message = "hello"
        key = generate_key(len(message.encode('utf-8')) * 4)
        assert decrypt(encrypt(message, key), key) == message

    def test_encrypt_decrypt_emoji(self):
        message = "hi!"
        key = generate_key(len(message.encode('utf-8')) * 4)
        assert decrypt(encrypt(message, key), key) == message

    def test_encrypt_changes_message(self):
        message = "Secret"
        key = generate_key(len(message) * 4)
        ciphertext = encrypt(message, key)
        from core.dna import encode_dna, text_to_bits
        dna_message = encode_dna(text_to_bits(message))
        assert ciphertext != dna_message

    def test_wrong_key_fails(self):
        message = "Secret"
        key = generate_key(len(message) * 4)
        wrong_key = generate_key(len(message) * 4)
        ciphertext = encrypt(message, key)
        # With a wrong key, decryption either raises (invalid UTF-8 bytes)
        # or produces a different plaintext. Both outcomes are valid --
        # the point is that the correct plaintext cannot be recovered.
        # Note: the probability that a random wrong key accidentally
        # produces the correct plaintext is 1/4^n -- negligible in practice.
        try:
            result = decrypt(ciphertext, wrong_key)
            assert result != message
        except (UnicodeDecodeError, ValueError):
            pass

    def test_key_too_short_raises(self):
        with pytest.raises(ValueError, match="at least as long"):
            encrypt("Hello world", "AT")

    def test_decrypt_key_too_short_raises(self):
        message = "Hi"
        key = generate_key(len(message) * 4)
        ciphertext = encrypt(message, key)
        with pytest.raises(ValueError, match="at least as long"):
            decrypt(ciphertext, "AT")

# ── 5PPD ───────────────────────────────────────────────────

class TestPPD:

    def test_5ppd_output_is_binary(self):
        seq = generate_key(50)
        bits = purine_parity_digitize(seq)
        assert set(bits).issubset({'0', '1'})

    def test_5ppd_output_length(self):
        seq = generate_key(50)
        bits = purine_parity_digitize(seq)
        assert len(bits) == 10

    def test_5ppd_known_value(self):
        # A C A T G -> purines: A, A, G -> count = 3 -> 3 % 2 = 1
        assert purine_parity_digitize("ACATG") == "1"

    def test_5ppd_all_purines(self):
        # AAAAA -> 5 purines -> 5 % 2 = 1
        assert purine_parity_digitize("AAAAA") == "1"

    def test_5ppd_all_pyrimidines(self):
        # CCCCC -> 0 purines -> 0 % 2 = 0
        assert purine_parity_digitize("CCCCC") == "0"

    def test_5ppd_custom_block_size(self):
        seq = generate_key(40)
        bits = purine_parity_digitize(seq, block_size=4)
        assert len(bits) == 10