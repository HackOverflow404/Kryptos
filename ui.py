"""
ui.py — Kryptos graphical interface
==========================================
Defines KryptosApp (the main Tk window) and all helper widget functions.
The UI delegates all encryption/decryption work to cipher.py — it never
touches the algorithm directly.
"""

import tkinter as tk
# from encryptor_complete import encrypt, decrypt
from encryptor import encrypt, decrypt

# ── theme constants ────────────────────────────────────────────────────────────

BG       = "#0d0d0d"
BG2      = "#141414"
BG3      = "#1c1c1c"
BORDER   = "#2e2e2e"
ACCENT   = "#e8c872"   # warm gold  — encrypt mode
ACCENT2  = "#c85a5a"   # muted red  — decrypt mode
TEXT     = "#e8e4da"
MUTED    = "#555"

MONO     = ("Courier New", 11)
MONO_LG  = ("Courier New", 13)
SANS_SM  = ("Courier New", 9)
TITLE_FN = ("Courier New", 22, "bold")
LABEL_FN = ("Courier New", 8)


# ── main application window ────────────────────────────────────────────────────

class KryptosApp(tk.Tk):
    """Root window for the Kryptos app."""

    def __init__(self):
        super().__init__()
        self.title("Kryptos")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(620, 560)
        self._build_ui()
        self._center_window(680, 640)

    # ── window helpers ─────────────────────────────────────────────────────────

    def _center_window(self, w: int, h: int) -> None:
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    # ── layout ─────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        self._build_header()
        sep(self, BORDER).pack(fill="x")
        self._build_body()
        sep(self, BORDER).pack(fill="x", pady=(12, 0))
        self._build_footer()

    def _build_header(self) -> None:
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x")

        tk.Canvas(hdr, height=3, bg=ACCENT, highlightthickness=0).pack(fill="x")

        inner = tk.Frame(hdr, bg=BG)
        inner.pack(fill="x", padx=28, pady=(18, 12))

        tk.Label(inner, text="Kryptos",   font=TITLE_FN, fg=ACCENT, bg=BG).pack(side="left")
        tk.Label(inner,
                 text="XOR + spiral keystream + bit-rotation",
                 font=LABEL_FN, fg=MUTED, bg=BG).pack(side="right", anchor="s", pady=6)

    def _build_body(self) -> None:
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=28, pady=20)
        body.columnconfigure(0, weight=1)

        # Mode toggle
        mode_row = tk.Frame(body, bg=BG)
        mode_row.grid(row=0, column=0, sticky="ew", pady=(0, 16))

        self.mode = tk.StringVar(value="encrypt")
        ModeButton(mode_row, "🔒  ENCRYPT", "encrypt",
                   self.mode, ACCENT,  self._refresh_mode).pack(side="left", padx=(0, 6))
        ModeButton(mode_row, "🔓  DECRYPT", "decrypt",
                   self.mode, ACCENT2, self._refresh_mode).pack(side="left")

        # Passphrase
        key_frame = labeled_frame(body, "PASSPHRASE  (your secret key)")
        key_frame.grid(row=1, column=0, sticky="ew", pady=(0, 14))

        self.key_var = tk.StringVar()
        self.key_entry = tk.Entry(
            key_frame, textvariable=self.key_var, show="●",
            font=MONO_LG, bg=BG3, fg=TEXT, insertbackground=ACCENT,
            relief="flat", bd=0,
            highlightthickness=1, highlightcolor=ACCENT, highlightbackground=BORDER,
        )
        self.key_entry.pack(fill="x", ipady=7, padx=1, pady=1)

        show_row = tk.Frame(key_frame, bg=BG2)
        show_row.pack(fill="x", padx=1)
        self.show_key = tk.BooleanVar()
        tk.Checkbutton(
            show_row, text="show passphrase", variable=self.show_key,
            command=self._toggle_show_key,
            bg=BG2, fg=MUTED, selectcolor=BG3,
            activebackground=BG2, activeforeground=MUTED,
            font=SANS_SM, bd=0, relief="flat", cursor="hand2",
        ).pack(side="left", pady=4, padx=6)

        # Input text area
        self.input_label_var = tk.StringVar(value="PLAINTEXT  (message to encrypt)")
        in_frame = labeled_frame_var(body, self.input_label_var)
        in_frame.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        self.input_text = scrolled_text(in_frame, height=5)

        # Run button
        self.run_btn = tk.Button(
            body, text="▶  ENCRYPT", command=self._run,
            font=("Courier New", 11, "bold"),
            bg=ACCENT, fg="#0d0d0d",
            relief="flat", bd=0, padx=20, pady=9, cursor="hand2",
            activebackground="#d4af58", activeforeground="#0d0d0d",
        )
        self.run_btn.grid(row=3, column=0, sticky="w", pady=(0, 14))

        # Output text area
        self.output_label_var = tk.StringVar(value="CIPHERTEXT  (hex-encoded output)")
        out_frame = labeled_frame_var(body, self.output_label_var)
        out_frame.grid(row=4, column=0, sticky="nsew")
        body.rowconfigure(4, weight=1)
        self.output_text = scrolled_text(out_frame, height=5, fg=ACCENT)
        self.output_text.configure(state="disabled")

        # Toolbar
        tb = tk.Frame(body, bg=BG)
        tb.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        small_btn(tb, "Copy output", self._copy_output).pack(side="left", padx=(0, 8))
        small_btn(tb, "Swap ↕",      self._swap        ).pack(side="left", padx=(0, 8))
        small_btn(tb, "Clear all",   self._clear       ).pack(side="left")

        self.status = tk.Label(tb, text="", font=SANS_SM, fg=MUTED, bg=BG)
        self.status.pack(side="right")

    def _build_footer(self) -> None:
        info = tk.Frame(self, bg=BG)
        info.pack(fill="x", padx=28, pady=(6, 10))
        tk.Label(
            info,
            text="Algorithm: spiral-keyed XOR  ·  bit-rotation by position  ·  UTF-8 safe  ·  output: hex",
            font=SANS_SM, fg=MUTED, bg=BG,
        ).pack(side="left")

    # ── event handlers ─────────────────────────────────────────────────────────

    def _refresh_mode(self) -> None:
        """Update labels and button colour when the mode toggle changes."""
        if self.mode.get() == "encrypt":
            self.run_btn.configure(text="▶  ENCRYPT", bg=ACCENT,
                                   activebackground="#d4af58")
            self.input_label_var.set("PLAINTEXT  (message to encrypt)")
            self.output_label_var.set("CIPHERTEXT  (hex-encoded output)")
        else:
            self.run_btn.configure(text="▶  DECRYPT", bg=ACCENT2,
                                   activebackground="#b04444")
            self.input_label_var.set("CIPHERTEXT  (hex pairs to decrypt)")
            self.output_label_var.set("PLAINTEXT  (decrypted message)")
        self._set_output("")

    def _run(self) -> None:
        """Call cipher.encrypt or cipher.decrypt and display the result."""
        key  = self.key_var.get()
        text = self.input_text.get("1.0", "end-1c")

        if not key:
            self._flash_status("⚠  Enter a passphrase first.", error=True)
            return
        if not text.strip():
            self._flash_status("⚠  Input is empty.", error=True)
            return

        try:
            if self.mode.get() == "encrypt":
                result = encrypt(text, key)
            else:
                result = decrypt(text, key)
            self._set_output(result)
            self._flash_status("✓  Done.")
        except Exception as exc:
            self._flash_status(f"✗  {exc}", error=True)

    def _copy_output(self) -> None:
        out = self.output_text.get("1.0", "end-1c")
        if out.strip():
            self.clipboard_clear()
            self.clipboard_append(out)
            self._flash_status("✓  Copied to clipboard.")
        else:
            self._flash_status("Nothing to copy.")

    def _swap(self) -> None:
        """Move the output into the input field and flip the mode."""
        out = self.output_text.get("1.0", "end-1c").strip()
        if not out:
            return
        new_mode = "decrypt" if self.mode.get() == "encrypt" else "encrypt"
        self.mode.set(new_mode)
        self._refresh_mode()
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", out)
        self._set_output("")

    def _clear(self) -> None:
        self.input_text.delete("1.0", "end")
        self._set_output("")
        self.key_var.set("")
        self.status.configure(text="")

    def _toggle_show_key(self) -> None:
        self.key_entry.configure(show="" if self.show_key.get() else "●")

    def _set_output(self, text: str) -> None:
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
        self.output_text.configure(state="disabled")

    def _flash_status(self, msg: str, error: bool = False) -> None:
        colour = ACCENT2 if error else "#6a9f6a"
        self.status.configure(text=msg, fg=colour)
        self.after(3000, lambda: self.status.configure(text=""))


# ── reusable widget helpers ────────────────────────────────────────────────────

def sep(parent: tk.Widget, color: str) -> tk.Canvas:
    """A 1-pixel horizontal separator line."""
    return tk.Canvas(parent, height=1, bg=color, highlightthickness=0)


def labeled_frame(parent: tk.Widget, title: str) -> tk.Frame:
    """A dark bordered frame with a small static label above the content."""
    outer = tk.Frame(parent, bg=BG2, highlightthickness=1,
                     highlightbackground=BORDER)
    tk.Label(outer, text=f" {title} ", font=LABEL_FN,
             fg=MUTED, bg=BG2).pack(anchor="w", padx=6, pady=(5, 0))
    return outer


def labeled_frame_var(parent: tk.Widget, textvariable: tk.StringVar) -> tk.Frame:
    """Like labeled_frame but the label text is bound to a StringVar."""
    outer = tk.Frame(parent, bg=BG2, highlightthickness=1,
                     highlightbackground=BORDER)
    tk.Label(outer, textvariable=textvariable, font=LABEL_FN,
             fg=MUTED, bg=BG2).pack(anchor="w", padx=6, pady=(5, 0))
    return outer


def scrolled_text(parent: tk.Widget, height: int = 4,
                  fg: str = TEXT) -> tk.Text:
    """A Text widget with an attached vertical scrollbar."""
    frame = tk.Frame(parent, bg=BG3)
    frame.pack(fill="both", expand=True, padx=1, pady=(0, 1))

    sb = tk.Scrollbar(frame, bg=BG3, troughcolor=BG3,
                      activebackground=BORDER, relief="flat", bd=0)
    sb.pack(side="right", fill="y")

    t = tk.Text(
        frame, height=height, font=MONO_LG,
        bg=BG3, fg=fg, insertbackground=ACCENT,
        relief="flat", bd=0, wrap="word",
        yscrollcommand=sb.set,
        selectbackground="#2e2e2e", selectforeground=TEXT,
        padx=10, pady=8, spacing1=2,
    )
    t.pack(side="left", fill="both", expand=True)
    sb.config(command=t.yview)
    return t


def small_btn(parent: tk.Widget, text: str, cmd) -> tk.Button:
    """A small, flat toolbar button."""
    return tk.Button(
        parent, text=text, command=cmd,
        font=SANS_SM, bg=BG3, fg=MUTED,
        relief="flat", bd=0, padx=10, pady=5, cursor="hand2",
        activebackground=BORDER, activeforeground=TEXT,
    )


class ModeButton(tk.Button):
    """A toggle button that highlights when its value matches the shared StringVar."""

    def __init__(self, parent, text: str, value: str,
                 variable: tk.StringVar, active_color: str, callback):
        super().__init__(parent, text=text,
                         font=("Courier New", 10, "bold"),
                         relief="flat", bd=0, padx=16, pady=7, cursor="hand2")
        self._var          = variable
        self._value        = value
        self._active_color = active_color
        self._callback     = callback
        self.configure(command=self._on_click)
        variable.trace_add("write", lambda *_: self._update())
        self._update()

    def _on_click(self) -> None:
        self._var.set(self._value)
        self._callback()

    def _update(self) -> None:
        active = self._var.get() == self._value
        self.configure(
            bg=self._active_color if active else BG3,
            fg="#0d0d0d"          if active else MUTED,
            activebackground=self._active_color,
            activeforeground="#0d0d0d",
        )