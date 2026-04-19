import tkinter as tk

_ACTIVE_SCROLL_TARGET = None
_BOUND_SCROLL_ROOTS = set()

BG_COLOR = "#0b1220"
SURFACE_COLOR = "#111a2b"
CARD_COLOR = "#182235"
CARD_ALT_COLOR = "#22314a"
BORDER_COLOR = "#314766"
ACCENT_COLOR = "#19b8ff"
ACCENT_HOVER = "#58d1ff"
ACCENT_SOFT = "#10374a"
TEXT_PRIMARY = "#f4f8fc"
TEXT_SECONDARY = "#c7d4e3"
TEXT_MUTED = "#8da3bc"
SUCCESS_COLOR = "#3bc48b"
WARNING_COLOR = "#f7c35f"
INPUT_BG = "#edf5fb"
INPUT_TEXT = "#122033"

HERO_FONT = ("Bahnschrift SemiBold", 30)
TITLE_FONT = ("Bahnschrift SemiBold", 24)
HEADING_FONT = ("Bahnschrift SemiBold", 16)
BODY_FONT = ("Corbel", 12)
SMALL_FONT = ("Corbel", 10)
BUTTON_FONT = ("Bahnschrift SemiBold", 11)


def style_root(root):
    root.configure(bg=BG_COLOR)


def clear_screen(root):
    for widget in root.winfo_children():
        widget.destroy()
    style_root(root)


def build_primary_button(parent, text, command, width=16):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        bg=ACCENT_COLOR,
        fg=BG_COLOR,
        activebackground=ACCENT_HOVER,
        activeforeground=BG_COLOR,
        font=BUTTON_FONT,
        relief="flat",
        bd=0,
        highlightbackground=ACCENT_COLOR,
        highlightcolor=ACCENT_COLOR,
        highlightthickness=1,
        cursor="hand2",
        padx=14,
        pady=11,
    )
    attach_hover(button, ACCENT_COLOR, ACCENT_HOVER, BG_COLOR, BG_COLOR)
    return button


def build_secondary_button(parent, text, command, width=16):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        bg=CARD_ALT_COLOR,
        fg=TEXT_PRIMARY,
        activebackground="#2a3c58",
        activeforeground=TEXT_PRIMARY,
        font=BUTTON_FONT,
        relief="flat",
        bd=0,
        highlightbackground=BORDER_COLOR,
        highlightcolor=ACCENT_COLOR,
        highlightthickness=1,
        cursor="hand2",
        padx=14,
        pady=11,
    )
    attach_hover(button, CARD_ALT_COLOR, "#2a3c58", TEXT_PRIMARY, TEXT_PRIMARY)
    return button


def build_badge(parent, text, bg=CARD_ALT_COLOR, fg=TEXT_SECONDARY):
    return tk.Label(
        parent,
        text=text,
        bg=bg,
        fg=fg,
        font=SMALL_FONT,
        padx=10,
        pady=5,
    )


def _is_descendant(widget, ancestor):
    while widget is not None:
        if str(widget) == str(ancestor):
            return True
        widget = getattr(widget, "master", None)
    return False


def _set_active_scroll_target(canvas, container):
    global _ACTIVE_SCROLL_TARGET
    _ACTIVE_SCROLL_TARGET = (canvas, container)


def _scroll_active_target(event):
    global _ACTIVE_SCROLL_TARGET

    if not _ACTIVE_SCROLL_TARGET:
        return None

    canvas, container = _ACTIVE_SCROLL_TARGET
    if not canvas.winfo_exists() or not container.winfo_exists():
        _ACTIVE_SCROLL_TARGET = None
        return None

    pointer_widget = container.winfo_containing(container.winfo_pointerx(), container.winfo_pointery())
    event_widget = getattr(event, "widget", None)
    if not (_is_descendant(pointer_widget, container) or _is_descendant(event_widget, container)):
        return None

    top_fraction, bottom_fraction = canvas.yview()
    if top_fraction <= 0.0 and bottom_fraction >= 1.0:
        return None

    if getattr(event, "delta", 0):
        step_size = max(1, int(abs(event.delta) / 120))
        direction = -1 if event.delta > 0 else 1
        canvas.yview_scroll(direction * step_size, "units")
        return "break"

    if getattr(event, "num", None) == 4:
        canvas.yview_scroll(-1, "units")
        return "break"

    if getattr(event, "num", None) == 5:
        canvas.yview_scroll(1, "units")
        return "break"

    return None


def _ensure_root_scroll_bindings(root):
    root_name = str(root)
    if root_name in _BOUND_SCROLL_ROOTS:
        return

    root.bind_all("<MouseWheel>", _scroll_active_target, add="+")
    root.bind_all("<Button-4>", _scroll_active_target, add="+")
    root.bind_all("<Button-5>", _scroll_active_target, add="+")
    _BOUND_SCROLL_ROOTS.add(root_name)


def build_scrollable_content(parent, bg=BG_COLOR):
    root = parent.winfo_toplevel()
    _ensure_root_scroll_bindings(root)

    container = tk.Frame(parent, bg=bg)
    canvas = tk.Canvas(
        container,
        bg=bg,
        bd=0,
        highlightthickness=0,
        yscrollincrement=20,
        takefocus=1,
    )
    scrollbar = tk.Scrollbar(
        container,
        orient="vertical",
        command=canvas.yview,
        bg=CARD_ALT_COLOR,
        activebackground=ACCENT_COLOR,
        troughcolor=bg,
        relief="flat",
        bd=0,
    )
    content = tk.Frame(canvas, bg=bg)
    bound_widgets = set()

    content_window = canvas.create_window((0, 0), window=content, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def sync_width(event):
        canvas.itemconfigure(content_window, width=event.width)
        update_scrollregion()

    def update_scrollregion(_event=None):
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def activate_scroll(_event=None):
        _set_active_scroll_target(canvas, container)

    def bind_scroll_activation(widget):
        widget_name = str(widget)
        if widget_name in bound_widgets:
            return

        widget.bind("<Enter>", activate_scroll, add="+")
        widget.bind("<Button-1>", activate_scroll, add="+")
        bound_widgets.add(widget_name)

        for child in widget.winfo_children():
            bind_scroll_activation(child)

    def on_key_scroll(event):
        activate_scroll()
        if event.keysym in {"Up", "KP_Up"}:
            canvas.yview_scroll(-1, "units")
            return "break"
        if event.keysym in {"Down", "KP_Down"}:
            canvas.yview_scroll(1, "units")
            return "break"
        if event.keysym in {"Prior", "KP_Prior"}:
            canvas.yview_scroll(-1, "pages")
            return "break"
        if event.keysym in {"Next", "KP_Next"}:
            canvas.yview_scroll(1, "pages")
            return "break"
        if event.keysym in {"Home", "KP_Home"}:
            canvas.yview_moveto(0)
            return "break"
        if event.keysym in {"End", "KP_End"}:
            canvas.yview_moveto(1)
            return "break"
        return None

    def refresh_content_bindings(_event=None):
        bind_scroll_activation(container)
        update_scrollregion()

    canvas.bind("<Configure>", sync_width)
    canvas.bind("<Up>", on_key_scroll, add="+")
    canvas.bind("<Down>", on_key_scroll, add="+")
    canvas.bind("<Prior>", on_key_scroll, add="+")
    canvas.bind("<Next>", on_key_scroll, add="+")
    canvas.bind("<Home>", on_key_scroll, add="+")
    canvas.bind("<End>", on_key_scroll, add="+")
    content.bind("<Configure>", refresh_content_bindings, add="+")
    bind_scroll_activation(container)
    activate_scroll()

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return container, content


def attach_hover(widget, normal_bg, hover_bg, normal_fg=None, hover_fg=None):
    def on_enter(_event):
        widget.configure(
            bg=hover_bg,
            fg=hover_fg if hover_fg is not None else widget.cget("fg"),
        )

    def on_leave(_event):
        widget.configure(
            bg=normal_bg,
            fg=normal_fg if normal_fg is not None else widget.cget("fg"),
        )

    widget.bind("<Enter>", on_enter, add="+")
    widget.bind("<Leave>", on_leave, add="+")


def make_widget_clickable(widget, command):
    def handle_click(_event):
        command()

    widget.bind("<Button-1>", handle_click)
    try:
        widget.configure(cursor="hand2")
    except tk.TclError:
        pass


def make_descendants_clickable(parent, command, skip_classes=None):
    skip_classes = set(skip_classes or ())
    for child in parent.winfo_children():
        if child.winfo_class() not in skip_classes:
            make_widget_clickable(child, command)
        make_descendants_clickable(child, command, skip_classes)
