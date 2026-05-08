"""
widgets.py — Reusable UI building blocks for the Car Rental System.

Classes / helpers:
  StyledButton   – flat modern button with hover effect
  LabelEntry     – label + Entry pair
  LabelCombo     – label + Combobox pair
  CardFrame      – raised dark card container
  StatCard       – KPI stat card for dashboard
  make_treeview  – creates a scrollable Treeview inside a parent frame
  refresh_tree   – clears & repopulates a Treeview
  make_search_bar – search input + button row
"""

import tkinter as tk
from tkinter import ttk
from .theme import COLORS, FONTS, PAD


# ══════════════════════════════════════════════════════════════════════════════
#  StyledButton
# ══════════════════════════════════════════════════════════════════════════════

class StyledButton(tk.Button):
    """A flat, modern button with smooth hover effect."""

    PRESETS = {
        "primary": (COLORS["accent"],   COLORS["accent_hover"],   COLORS["text_primary"]),
        "success": (COLORS["success"],  COLORS["success_hover"],  COLORS["text_primary"]),
        "danger":  (COLORS["danger"],   COLORS["danger_hover"],   COLORS["text_primary"]),
        "warning": (COLORS["warning"],  COLORS["warning_hover"],  "#1A1D27"),
        "neutral": (COLORS["bg_tertiary"], COLORS["border"],      COLORS["text_primary"]),
        "teal":    (COLORS["teal"],     "#17A589",                COLORS["text_primary"]),
        "purple":  (COLORS["purple"],   "#8E44AD",                COLORS["text_primary"]),
        "gold":    (COLORS["gold"],     "#D4AC0D",                "#1A1D27"),
    }

    def __init__(self, parent, text, command=None, style="primary",
                 width=None, padx=16, pady=8, **kwargs):
        bg, hover, fg = self.PRESETS.get(style, self.PRESETS["primary"])
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg, fg=fg,
            activebackground=hover,
            activeforeground=fg,
            font=FONTS["button"],
            relief="flat",
            cursor="hand2",
            padx=padx,
            pady=pady,
            **kwargs,
        )
        if width:
            self.config(width=width)
        self._bg, self._hover = bg, hover
        self.bind("<Enter>", lambda e: self.config(bg=self._hover))
        self.bind("<Leave>", lambda e: self.config(bg=self._bg))


# ══════════════════════════════════════════════════════════════════════════════
#  LabelEntry
# ══════════════════════════════════════════════════════════════════════════════

class LabelEntry(tk.Frame):
    """Label + Entry combo that returns a StringVar."""

    def __init__(self, parent, label, show=None, width=26, **kwargs):
        super().__init__(parent, bg=COLORS["bg_secondary"], **kwargs)
        tk.Label(
            self, text=label,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_secondary"],
            font=FONTS["small"],
            anchor="w",
        ).pack(fill="x", pady=(0, 2))

        self.var = tk.StringVar()
        entry = tk.Entry(
            self,
            textvariable=self.var,
            show=show,
            bg=COLORS["bg_tertiary"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["accent"],
            relief="flat",
            font=FONTS["body"],
            width=width,
        )
        entry.pack(fill="x", ipady=6)
        # thin accent underline on focus
        entry.bind("<FocusIn>",  lambda e: entry.config(bg="#2D3057"))
        entry.bind("<FocusOut>", lambda e: entry.config(bg=COLORS["bg_tertiary"]))

    def get(self):
        return self.var.get().strip()

    def set(self, val):
        self.var.set(val)

    def clear(self):
        self.var.set("")


# ══════════════════════════════════════════════════════════════════════════════
#  LabelCombo
# ══════════════════════════════════════════════════════════════════════════════

class LabelCombo(tk.Frame):
    """Label + ttk.Combobox pair."""

    def __init__(self, parent, label, values=None, width=24, **kwargs):
        super().__init__(parent, bg=COLORS["bg_secondary"], **kwargs)
        tk.Label(
            self, text=label,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_secondary"],
            font=FONTS["small"],
            anchor="w",
        ).pack(fill="x", pady=(0, 2))

        self.var = tk.StringVar()
        style = ttk.Style()
        style.configure("Dark.TCombobox",
                         fieldbackground=COLORS["bg_tertiary"],
                         background=COLORS["bg_tertiary"],
                         foreground=COLORS["text_primary"],
                         arrowcolor=COLORS["accent"],
                         selectbackground=COLORS["table_select"],
                         selectforeground=COLORS["text_primary"])

        self.combo = ttk.Combobox(
            self,
            textvariable=self.var,
            values=values or [],
            state="readonly",
            width=width,
            style="Dark.TCombobox",
            font=FONTS["body"],
        )
        self.combo.pack(fill="x", ipady=4)

    def get(self):
        return self.var.get().strip()

    def set(self, val):
        self.var.set(val)

    def clear(self):
        self.var.set("")

    def set_values(self, values):
        self.combo["values"] = values


# ══════════════════════════════════════════════════════════════════════════════
#  CardFrame
# ══════════════════════════════════════════════════════════════════════════════

class CardFrame(tk.Frame):
    """Raised card with rounded visual appearance."""

    def __init__(self, parent, title=None, **kwargs):
        super().__init__(
            parent,
            bg=COLORS["bg_secondary"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            **kwargs,
        )
        if title:
            tk.Label(
                self, text=title,
                bg=COLORS["bg_secondary"],
                fg=COLORS["text_secondary"],
                font=FONTS["subheading"],
            ).pack(anchor="w", padx=PAD["md"], pady=(PAD["sm"], 0))


# ══════════════════════════════════════════════════════════════════════════════
#  StatCard
# ══════════════════════════════════════════════════════════════════════════════

class StatCard(tk.Frame):
    """KPI tile: coloured accent bar, big number, label, icon."""

    def __init__(self, parent, label, icon="📊", accent=None, **kwargs):
        accent = accent or COLORS["accent"]
        super().__init__(
            parent,
            bg=COLORS["bg_secondary"],
            highlightbackground=accent,
            highlightthickness=2,
            **kwargs,
        )
        # left accent bar
        tk.Frame(self, bg=accent, width=5).pack(side="left", fill="y")

        inner = tk.Frame(self, bg=COLORS["bg_secondary"], padx=PAD["lg"], pady=PAD["lg"])
        inner.pack(fill="both", expand=True)

        # icon + label row
        top_row = tk.Frame(inner, bg=COLORS["bg_secondary"])
        top_row.pack(fill="x")
        tk.Label(top_row, text=icon,  bg=COLORS["bg_secondary"], font=("Segoe UI Emoji", 18)).pack(side="left")
        tk.Label(top_row, text=label, bg=COLORS["bg_secondary"],
                 fg=COLORS["text_secondary"], font=FONTS["stat_label"]).pack(side="left", padx=6)

        # big number
        self.value_lbl = tk.Label(
            inner, text="0",
            bg=COLORS["bg_secondary"],
            fg=accent,
            font=FONTS["stat_number"],
        )
        self.value_lbl.pack(anchor="w")

    def set_value(self, val):
        self.value_lbl.config(text=str(val))


# ══════════════════════════════════════════════════════════════════════════════
#  Treeview factory
# ══════════════════════════════════════════════════════════════════════════════

def make_treeview(parent, columns, heights=18):
    """
    Build and return a scrollable ttk.Treeview inside *parent*.

    Returns (tree, frame) — caller should pack/grid the frame.
    """
    container = tk.Frame(parent, bg=COLORS["bg_primary"])

    tree = ttk.Treeview(
        container,
        columns=columns,
        show="headings",
        height=heights,
        selectmode="browse",
    )

    vsb = ttk.Scrollbar(container, orient="vertical",   command=tree.yview)
    hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # layout
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    # column headings
    for col in columns:
        tree.heading(col, text=col, anchor="w")
        tree.column(col, anchor="w", minwidth=80, width=120)

    # alternating row tags
    tree.tag_configure("odd",  background=COLORS["table_odd"])
    tree.tag_configure("even", background=COLORS["table_even"])

    return tree, container


def refresh_tree(tree, rows):
    """Clear *tree* and insert *rows* (list of tuples/lists) with alt colours."""
    tree.delete(*tree.get_children())
    for i, row in enumerate(rows):
        tag = "odd" if i % 2 == 0 else "even"
        tree.insert("", "end", values=list(row), tags=(tag,))


# ══════════════════════════════════════════════════════════════════════════════
#  Search bar helper
# ══════════════════════════════════════════════════════════════════════════════

def make_search_bar(parent, search_cmd, placeholder="Search…"):
    """
    Returns (frame, StringVar) — frame contains entry + button.
    Caller packs/grids the frame.
    """
    frame = tk.Frame(parent, bg=COLORS["bg_primary"])
    var = tk.StringVar()

    entry = tk.Entry(
        frame,
        textvariable=var,
        bg=COLORS["bg_tertiary"],
        fg=COLORS["text_primary"],
        insertbackground=COLORS["accent"],
        relief="flat",
        font=FONTS["body"],
        width=30,
    )
    entry.insert(0, placeholder)
    entry.config(fg=COLORS["text_muted"])

    def _on_focus_in(e):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg=COLORS["text_primary"])

    def _on_focus_out(e):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg=COLORS["text_muted"])

    entry.bind("<FocusIn>",  _on_focus_in)
    entry.bind("<FocusOut>", _on_focus_out)
    entry.bind("<Return>",   lambda e: search_cmd())

    entry.pack(side="left", ipady=7, padx=(0, 6))

    StyledButton(frame, "🔍  Search", command=search_cmd,
                 style="primary", pady=6).pack(side="left")

    return frame, var
