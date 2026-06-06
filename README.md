# Kryptos — CS 124 Honors Cybersecurity Workshop

A hands-on cryptography project built for the CS 124 Honors section workshop at UIUC.

## What it is

Kryptos is a desktop encryption/decryption app that implements a custom symmetric cipher from scratch. The goal is to learn core cryptographic concepts by building (and partially filling in) the algorithm yourself.

The cipher combines three layers:

1. **Spiral keystream** — a passphrase-derived stream of pseudo-random bytes where each byte feeds back into the next, so the stream continuously evolves even when the key cycles.
2. **XOR** — each plaintext byte is XOR'd with its corresponding keystream byte. XOR is its own inverse, so the same operation encrypts and decrypts.
3. **Bit rotation** — each byte is rotated left/right by its position index (mod 8), adding position-dependence so identical plaintext bytes at different positions produce different ciphertext bytes.

Output is encoded as space-separated uppercase hex pairs (e.g. `3F A2 DE`).

## Project structure

```
main.py              entry point — launches the Tkinter GUI
ui.py                graphical interface (Kryptos app window)
encryptor.py         fill-in-the-blank learning version of the cipher
encryptor_complete.py  complete reference implementation
```

## Running it

```bash
python main.py
```

Requires Python 3.10+ and Tkinter (included with most Python installs).

## Workshop goal

`encryptor.py` is the annotated learning version — each function has explanations and marked blanks. Fill in the blanks, then swap the import in `ui.py` from `encryptor_complete` to `encryptor` to test your implementation against the live app.
