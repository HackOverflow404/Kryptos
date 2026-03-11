"""
main.py — Kryptos App entry point
=====================================
Run this file to launch the application:

    python main.py

Project layout
--------------
    main.py    ← you are here  (entry point)
    ui.py      ← Tkinter window and all widgets
    encryptor.py  ← encryption / decryption logic (no UI dependencies)
"""

from ui import KryptosApp


def main() -> None:
    app = KryptosApp()
    app.mainloop()


if __name__ == "__main__":
    main()