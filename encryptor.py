"""
cipher.py — Prism Cipher core logic (ANNOTATED LEARNING VERSION)
=================================================================
This file walks through each concept with explanations and blanks
for the key implementation details. Fill in the [ ? ] sections to
test your understanding, then compare against the working version.
"""

import re

# ══════════════════════════════════════════════════════════════════
# CONCEPT 1 — CONSTANTS
# ══════════════════════════════════════════════════════════════════
#
# We need two "magic numbers" that stay fixed for all time.
#
# PRIME_STEP: multiplied against each key character before mixing.
#   WHY A PRIME? Primes don't share factors with 256 (our byte range),
#   so multiplying by a prime before masking with & 0xFF distributes
#   values more evenly — you avoid clustering around multiples of 2.
#   Try changing this to an even number and see how patterns emerge.
#
#   Rule of thumb: pick any prime > 10 and < 256.
#   Examples: 17, 31, 37, 53, 97 all work well.
#   PRIME_STEP = [ pick a prime number between 10 and 100 ]
#
# SPIRAL_SEED: the very first "prev" value before any key bytes are mixed.
#   WHY NON-ZERO? If prev starts at 0 and the first key byte is also 0,
#   the first keystream byte would be 0 — XOR with 0 means no encryption.
#   Any non-zero value breaks this weakness.
#   SPIRAL_SEED = [ pick any hex value from 0x01 to 0xFF, e.g. 0xA5 ]

PRIME_STEP  = 31
SPIRAL_SEED = 0xA5


# ══════════════════════════════════════════════════════════════════
# CONCEPT 2 — THE SPIRAL KEYSTREAM
# ══════════════════════════════════════════════════════════════════
#
# WHAT IS A KEYSTREAM?
#   A keystream is a sequence of pseudo-random bytes derived from your
#   passphrase. Each byte in your message gets paired with one keystream
#   byte. The keystream must be:
#     - Deterministic: same key → same stream, every time (so decryption works)
#     - Sensitive to the key: changing one character should cascade changes
#       through the whole stream
#
# HOW THE SPIRAL WORKS (one step):
#
#   prev  ──────────────────────────────────────────┐
#                                                   ▼
#   key_byte  ──► × PRIME_STEP ──► + position ──► XOR ──► & 0xFF ──► val
#                                                                       │
#                                                   ┌───────────────────┘
#                                                   ▼
#                                                 new prev
#
#   In Python: val = (prev ^ (kb * PRIME_STEP + i)) & 0xFF
#
#   The "spiral" name comes from how `val` feeds back into `prev`:
#   each output depends on all previous outputs, so the stream doesn't
#   simply repeat with the key period — it continuously evolves.
#
# KEY CYCLING:
#   If the message is longer than the key, we wrap around using modulo:
#   kb = key_bytes[ i % len(key_bytes) ]
#   A 4-character key for a 100-byte message cycles through its
#   characters 25 times — but the spiral ensures different output each cycle.

def _generate_keystream(key: str, length: int) -> list[int]:
    if not key:
        raise ValueError("Passphrase must not be empty.")

    # Step 1: Convert each passphrase character to its ASCII/Unicode number.
    #   ord('A') = 65,  ord('z') = 122,  ord('!') = 33
    #   [ convert each character in `key` to an int using ord() ]
    key_bytes = [ord(c) for c in key]

    stream: list[int] = []

    # Step 2: Initialise `prev` to our non-zero seed.
    #   [ set prev = SPIRAL_SEED ]
    prev = SPIRAL_SEED

    for i in range(length):
        # Step 3: Pick the key byte for this position, cycling if needed.
        #   [ kb = key_bytes at index (i mod key length) ]
        kb = key_bytes[i % len(key_bytes)]

        # Step 4: Compute this keystream byte.
        #   Mix kb, the step index, and the previous output together.
        #   XOR (^) combines bits. & 0xFF clamps to 8 bits (0–255).
        #   [ val = (prev XOR (kb * PRIME_STEP + i)) & 0xFF ]
        val = (prev ^ (kb * PRIME_STEP + i)) & 0xFF

        stream.append(val)

        # Step 5: The feedback loop — this output becomes next round's `prev`.
        #   [ prev = val ]
        prev = val

    return stream


# ══════════════════════════════════════════════════════════════════
# CONCEPT 3 — BIT ROTATION
# ══════════════════════════════════════════════════════════════════
#
# WHAT IS BIT ROTATION?
#   Imagine a byte as 8 bits in a circle. Rotating LEFT by n means
#   shifting all bits n places to the left, and the bits that "fall off"
#   the left edge wrap around to the right end.
#
#   Example — rotate 0b11010010 left by 2:
#     Original:  1 1 0 1 0 0 1 0
#     Shift L2:  0 1 0 0 1 0 | 1 1   ← the two 1s wrap around
#     Result:    0 1 0 0 1 0 1 1  =  0b01001011
#
# WHY DO WE ROTATE (and not just XOR)?
#   XOR alone: if two plaintext bytes are identical AND their keystream
#   bytes happen to be the same, the ciphertext bytes will be identical —
#   a pattern an attacker could exploit.
#
#   Rotation adds position-dependence: byte at position 0 rotates by 0,
#   position 1 rotates by 1, ..., position 7 rotates by 7, position 8
#   wraps back to 0, etc.  Same input byte at different positions →
#   different output. This breaks the pattern.
#
# THE FORMULA:
#   Rotate LEFT  by n:  ((byte << n) | (byte >> (8 - n))) & 0xFF
#   Rotate RIGHT by n:  ((byte >> n) | (byte << (8 - n))) & 0xFF
#
#   LEFT SHIFT  (<<): moves bits toward the high end, vacates the right
#   RIGHT SHIFT (>>): moves bits toward the low end, vacates the left
#   OR (|):           combines both halves back into one byte
#   & 0xFF:           discards any bits above position 7

def _rotate_left(byte: int, n: int) -> int:
    # Clamp n to 0–7 (rotating by 8 is the same as rotating by 0)
    # [ n = n mod 8 ]
    n = n % 8

    # Combine the left-shifted part and the wrapped-around right part.
    # [ return ((byte << n) OR (byte >> (8 - n))) AND 0xFF ]
    return ((byte << n) | (byte >> (8 - n))) & 0xFF


def _rotate_right(byte: int, n: int) -> int:
    # Mirror of rotate_left — shift right, wrap the fallen-off bits to the left.
    # [ n = n mod 8 ]
    n = n % 8

    # [ return ((byte >> n) OR (byte << (8 - n))) AND 0xFF ]
    return ((byte >> n) | (byte << (8 - n))) & 0xFF


# ══════════════════════════════════════════════════════════════════
# CONCEPT 4 — ENCRYPTION (combining all three layers)
# ══════════════════════════════════════════════════════════════════
#
# FLOW FOR EACH BYTE AT POSITION i:
#
#   plaintext_byte
#       │
#       ▼
#   XOR with keystream[i]        ← layer 1: scramble the value
#       │
#       ▼
#   rotate_left by (i % 8)       ← layer 2: scramble based on position
#       │
#       ▼
#   ciphertext_byte
#
# OUTPUT FORMAT:
#   Raw bytes aren't safe to paste into a text field or share in a
#   message — they may contain invisible control characters or invalid
#   UTF-8 sequences. So we encode each byte as a 2-digit uppercase hex
#   string and join them with spaces:  [0xDE, 0xB6] → "DE B6"
#
#   f"{b:02X}" means: format as uppercase hex, minimum 2 digits, zero-padded.
#   So 5 → "05",  255 → "FF",  171 → "AB"

def encrypt(plaintext: str, key: str) -> str:
    # Step 1: Encode the string to raw bytes (UTF-8 handles emoji, accents, etc.)
    #   [ data = plaintext encoded as UTF-8 bytes ]
    data = plaintext.encode("utf-8")

    # Step 2: Generate one keystream byte for every plaintext byte.
    #   [ stream = _generate_keystream(key, len(data)) ]
    stream = _generate_keystream(key, len(data))

    out = []

    for i, (byte, ks) in enumerate(zip(data, stream)):
        # Step 3: XOR the plaintext byte with the keystream byte.
        #   XOR truth table: same bits → 0, different bits → 1
        #   Crucially: (A XOR B) XOR B = A  ← this is why decryption is identical
        #   [ xored = byte XOR ks ]
        xored = byte ^ ks

        # Step 4: Rotate left by position to add position-dependence.
        #   [ rotated = _rotate_left(xored, i mod 8) ]
        rotated = _rotate_left(xored, i % 8)

        out.append(rotated)

    # Step 5: Format as space-separated uppercase hex pairs.
    #   [ return each byte in `out` formatted as a 2-digit uppercase hex, joined by spaces ]
    return " ".join(f"{b:02X}" for b in out)


# ══════════════════════════════════════════════════════════════════
# CONCEPT 5 — DECRYPTION (strict reversal of encryption)
# ══════════════════════════════════════════════════════════════════
#
# DECRYPTION MUST REVERSE ENCRYPTION IN EXACT OPPOSITE ORDER:
#
#   ciphertext_byte
#       │
#       ▼
#   rotate_RIGHT by (i % 8)      ← undo layer 2 first
#       │
#       ▼
#   XOR with keystream[i]        ← undo layer 1 (XOR is self-inverse)
#       │
#       ▼
#   plaintext_byte
#
# WHY XOR IS ITS OWN INVERSE:
#   Encrypting:   plain  XOR key = cipher
#   Decrypting:   cipher XOR key = plain   ← same operation!
#   Proof: (plain XOR key) XOR key = plain XOR (key XOR key) = plain XOR 0 = plain
#
# WHY ROTATION ORDER MATTERS:
#   We rotated LEFT during encryption, so we must rotate RIGHT first
#   before XOR-ing. Doing it in the wrong order gives garbage output.
#
# INPUT VALIDATION:
#   We validate the ciphertext is well-formed hex before processing —
#   this gives a clear error message rather than a cryptic crash.

def decrypt(ciphertext: str, key: str) -> str:
    # Step 1: Split the hex string into individual tokens.
    #   "DE B6 F6" → ["DE", "B6", "F6"]
    #   [ hex_tokens = ciphertext stripped and split on whitespace ]
    hex_tokens = ciphertext.strip().split()

    if not hex_tokens:
        raise ValueError("Ciphertext is empty.")

    # Step 2: Validate — every token must be exactly 2 hex characters.
    #   re.fullmatch(r"[0-9A-Fa-f]{2}", t) matches "3F" but not "3", "3FF", or "ZZ"
    #   [ check all tokens match the pattern, raise ValueError if not ]
    if not all(re.fullmatch(r"[0-9A-Fa-f]{2}", t) for t in hex_tokens):
        raise ValueError(
            "Ciphertext must be space-separated hex pairs (e.g. 3F A2 …)."
        )

    # Step 3: Convert each hex string back to an integer.
    #   int("DE", 16) = 222,  int("B6", 16) = 182
    #   [ data = list of ints, each parsed from hex with base 16 ]
    data = [int(t, 16) for t in hex_tokens]

    # Step 4: Regenerate the exact same keystream (same key + same length = same stream).
    #   [ stream = _generate_keystream(key, len(data)) ]
    stream = _generate_keystream(key, len(data))

    out = []

    for i, (byte, ks) in enumerate(zip(data, stream)):
        # Step 5: Undo the rotation FIRST (reverse of encryption's step 4).
        #   [ unrotated = _rotate_right(byte, i mod 8) ]
        unrotated = _rotate_right(byte, i % 8)

        # Step 6: XOR with the keystream to recover the original byte.
        #   (cipher XOR key) XOR key = plain
        #   [ plain_byte = unrotated XOR ks ]
        plain_byte = unrotated ^ ks

        out.append(plain_byte)

    # Step 7: Decode the byte sequence back to a UTF-8 string.
    #   If the wrong key was used, the bytes won't be valid UTF-8 → UnicodeDecodeError
    #   [ return bytes(out) decoded as UTF-8 ]
    return bytes(out).decode("utf-8")