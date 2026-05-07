"""
theme.py — Color palette, fonts, and sizing constants for the Car Rental System GUI.
All GUI modules import from here so the design stays consistent.
"""

# ─── Color Palette (Dark Theme) ───────────────────────────────────────────────
COLORS = {
    "bg_primary":     "#0F1117",   # deepest background
    "bg_secondary":   "#1A1D27",   # card / panel background
    "bg_tertiary":    "#252836",   # input / inner panel
    "accent":         "#4F8EF7",   # primary action blue
    "accent_hover":   "#3A7DE8",
    "success":        "#2ECC71",
    "success_hover":  "#27AE60",
    "warning":        "#F39C12",
    "warning_hover":  "#E67E22",
    "danger":         "#E74C3C",
    "danger_hover":   "#C0392B",
    "text_primary":   "#EAEAEA",
    "text_secondary": "#9BA3B2",
    "text_muted":     "#5C6370",
    "border":         "#2E3244",
    "table_odd":      "#1E2132",
    "table_even":     "#1A1D27",
    "table_select":   "#2D3561",
    "gold":           "#F1C40F",
    "teal":           "#1ABC9C",
    "purple":         "#9B59B6",
}

# ─── Fonts ────────────────────────────────────────────────────────────────────
FONTS = {
    "title":       ("Segoe UI", 22, "bold"),
    "heading":     ("Segoe UI", 14, "bold"),
    "subheading":  ("Segoe UI", 11, "bold"),
    "body":        ("Segoe UI", 10),
    "body_bold":   ("Segoe UI", 10, "bold"),
    "small":       ("Segoe UI", 9),
    "mono":        ("Consolas", 10),
    "stat_number": ("Segoe UI", 28, "bold"),
    "stat_label":  ("Segoe UI", 9),
    "button":      ("Segoe UI", 10, "bold"),
    "login_title": ("Segoe UI", 26, "bold"),
}

# ─── Spacing ──────────────────────────────────────────────────────────────────
PAD = {
    "xs":  4,
    "sm":  8,
    "md":  12,
    "lg":  16,
    "xl":  24,
    "xxl": 36,
}

# ─── Treeview tag colours (alternating rows + selection) ─────────────────────
def apply_treeview_style(style_obj):
    """Configure ttk.Style for all Treeview widgets globally."""
    style_obj.theme_use("clam")

    style_obj.configure(
        "Treeview",
        background=COLORS["bg_secondary"],
        foreground=COLORS["text_primary"],
        fieldbackground=COLORS["bg_secondary"],
        rowheight=30,
        font=FONTS["body"],
        borderwidth=0,
    )
    style_obj.configure(
        "Treeview.Heading",
        background=COLORS["bg_tertiary"],
        foreground=COLORS["accent"],
        font=FONTS["body_bold"],
        relief="flat",
        padding=(8, 6),
    )
    style_obj.map(
        "Treeview",
        background=[("selected", COLORS["table_select"])],
        foreground=[("selected", COLORS["text_primary"])],
    )
    style_obj.map(
        "Treeview.Heading",
        background=[("active", COLORS["border"])],
    )

    # Scrollbar
    style_obj.configure(
        "Vertical.TScrollbar",
        background=COLORS["bg_tertiary"],
        troughcolor=COLORS["bg_primary"],
        arrowcolor=COLORS["text_secondary"],
        borderwidth=0,
    )
    style_obj.configure(
        "Horizontal.TScrollbar",
        background=COLORS["bg_tertiary"],
        troughcolor=COLORS["bg_primary"],
        arrowcolor=COLORS["text_secondary"],
        borderwidth=0,
    )
