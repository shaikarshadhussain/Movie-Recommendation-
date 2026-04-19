import os
import re
import tkinter as tk
import math

POSTER_DIR = os.path.join(os.path.dirname(__file__), "assets", "posters")
POSTER_EXTENSIONS = (".png", ".jpg", ".jpeg")
POSTER_SIZES = {
    "hero": (180, 270),
    "card": (120, 180),
    "featured": (120, 180),
    "detail": (180, 270),
}
_POSTER_CACHE = {}


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def get_poster_path(movie):
    base_name = slugify(movie["title"])
    for extension in POSTER_EXTENSIONS:
        path = os.path.join(POSTER_DIR, f"{base_name}{extension}")
        if os.path.exists(path):
            return path
    return os.path.join(POSTER_DIR, f"{base_name}.png")


def get_poster_image(movie, variant="card"):
    path = get_poster_path(movie)
    if not os.path.exists(path):
        return None

    cache_key = (path, variant)
    if cache_key in _POSTER_CACHE:
        return _POSTER_CACHE[cache_key]

    image = tk.PhotoImage(file=path)
    target_width, target_height = POSTER_SIZES.get(variant, (120, 180))
    scale = max(
        1,
        math.ceil(
            max(
                image.width() / target_width,
                image.height() / target_height,
            )
        ),
    )
    if scale > 1:
        image = image.subsample(scale, scale)

    _POSTER_CACHE[cache_key] = image
    return image


def build_poster_widget(parent, movie, variant="card", bg="#182235"):
    width, height = POSTER_SIZES.get(variant, (120, 180))
    frame = tk.Frame(parent, bg=bg, width=width, height=height)
    frame.pack_propagate(False)

    image = get_poster_image(movie, variant)
    if image:
        label = tk.Label(frame, image=image, bg=bg, bd=0, highlightthickness=0)
        label.image = image
        label.pack(fill="both", expand=True)
    else:
        tk.Label(
            frame,
            text=movie["title"],
            bg=bg,
            fg="#f4f8fc",
            wraplength=width - 20,
            justify="center",
            font=("Bahnschrift SemiBold", 12),
            padx=10,
            pady=10,
        ).pack(fill="both", expand=True)

    return frame
