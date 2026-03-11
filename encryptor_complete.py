"""
cipher.py — Prism Cipher core logic
====================================
The Prism Cipher is a symmetric encryption scheme built from three layers:

  1. Spiral Keystream  — the passphrase is expanded into a pseudo-random
     byte stream.  Each byte is:
         val = (prev XOR (key_byte * PRIME_STEP + position)) & 0xFF
     where `prev` starts at SPIRAL_SEED and is updated every step.

  2. XOR encryption    — each plaintext byte is XOR'd with the next
     keystream byte.  Decryption is identical (XOR is its own inverse).

  3. Bit rotation      — after XOR, each byte is rotated LEFT by
     (position % 8) bits.  This means two identical plaintext bytes at
     different positions always produce different ciphertext bytes,
     defeating simple frequency analysis.

Decryption reverses step 3 (rotate RIGHT) then step 2 (XOR again).
Output is space-separated uppercase hex pairs, e.g.  "3F A2 D1 …"
"""

import re

# ── constants ──────────────────────────────────────────────────────────────────

PRIME_STEP   = 31
SPIRAL_SEED  = 0xA5   # arbitrary non-zero starting value for the spiral


# ── internal helpers ───────────────────────────────────────────────────────────

def _generate_keystream(key: str, length: int) -> list[int]:
    """
    Expand *key* into a deterministic pseudo-random byte list of *length*.

    Args:
        key:    Non-empty passphrase string.
        length: Number of keystream bytes needed.

    Returns:
        List of ints in range [0, 255].

    Raises:
        ValueError: if *key* is empty.
    """
    if not key:
        raise ValueError("Passphrase must not be empty.")

    key_bytes = [ord(c) for c in key]
    stream: list[int] = []
    prev = SPIRAL_SEED

    for i in range(length):
        kb  = key_bytes[i % len(key_bytes)]
        val = (prev ^ (kb * PRIME_STEP + i)) & 0xFF
        stream.append(val)
        prev = val

    return stream


def _rotate_left(byte: int, n: int) -> int:
    """Rotate an 8-bit integer left by *n* bit positions."""
    n = n % 8
    return ((byte << n) | (byte >> (8 - n))) & 0xFF


def _rotate_right(byte: int, n: int) -> int:
    """Rotate an 8-bit integer right by *n* bit positions (inverse of left)."""
    n = n % 8
    return ((byte >> n) | (byte << (8 - n))) & 0xFF


# ── public API ─────────────────────────────────────────────────────────────────

def encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt *plaintext* with the Prism Cipher using *key*.

    Args:
        plaintext: Any UTF-8 string.
        key:       Non-empty passphrase.

    Returns:
        Uppercase hex string, e.g. "DE B6 F6 1C …"

    Raises:
        ValueError: if *key* is empty.
    """
    data   = plaintext.encode("utf-8")
    stream = _generate_keystream(key, len(data))
    out    = []

    for i, (byte, ks) in enumerate(zip(data, stream)):
        xored   = byte ^ ks
        rotated = _rotate_left(xored, i % 8)
        out.append(rotated)

    return " ".join(f"{b:02X}" for b in out)


def decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt a hex-encoded Prism Cipher string back to plaintext.

    Args:
        ciphertext: Space-separated hex pairs produced by :func:`encrypt`.
        key:        The same passphrase used during encryption.

    Returns:
        Original UTF-8 plaintext.

    Raises:
        ValueError: if *ciphertext* is not valid hex pairs, or *key* is empty.
        UnicodeDecodeError: if the key is wrong (garbled bytes are not valid UTF-8).
    """
    hex_tokens = ciphertext.strip().split()

    if not hex_tokens:
        raise ValueError("Ciphertext is empty.")

    if not all(re.fullmatch(r"[0-9A-Fa-f]{2}", t) for t in hex_tokens):
        raise ValueError(
            "Ciphertext must be space-separated hex pairs (e.g. 3F A2 …)."
        )

    data   = [int(t, 16) for t in hex_tokens]
    stream = _generate_keystream(key, len(data))
    out    = []

    for i, (byte, ks) in enumerate(zip(data, stream)):
        unrotated  = _rotate_right(byte, i % 8)
        plain_byte = unrotated ^ ks
        out.append(plain_byte)

    return bytes(out).decode("utf-8")