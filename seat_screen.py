import tkinter as tk
from tkinter import messagebox

from booking import open_link, open_primary_link
from database import get_movie, get_platform_links, get_mood_option
from poster_utils import build_poster_widget
from theme import (
    ACCENT_COLOR,
    ACCENT_SOFT,
    BG_COLOR,
    BODY_FONT,
    CARD_ALT_COLOR,
    CARD_COLOR,
    HEADING_FONT,
    SMALL_FONT,
    SUCCESS_COLOR,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TITLE_FONT,
    build_badge,
    build_primary_button,
    build_scrollable_content,
    build_secondary_button,
    clear_screen,
    make_descendants_clickable,
    make_widget_clickable,
)


def show_watch_options(root, movie_id, mood_key=None):
    clear_screen(root)

    movie = get_movie(movie_id)
    links = get_platform_links(movie_id)
    mood = get_mood_option(mood_key) if mood_key else None

    if not movie:
        tk.Label(
            root,
            text="Movie details not found.",
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
            font=BODY_FONT,
        ).pack(pady=40)
        return

    root.title(f"{movie['title']} | Watch Online")

    page = tk.Frame(root, bg=BG_COLOR)
    page.pack(fill="both", expand=True)

    top_bar = tk.Frame(page, bg=BG_COLOR)
    top_bar.pack(fill="x", padx=24, pady=(18, 10))

    build_secondary_button(
        top_bar,
        "Back",
        command=lambda: go_back(root, mood_key),
        width=12,
    ).pack(side="left")
    tk.Label(
        top_bar,
        text="Every button opens directly in your browser",
        bg=BG_COLOR,
        fg=TEXT_MUTED,
        font=SMALL_FONT,
    ).pack(side="right")

    scroll_host, content = build_scrollable_content(page, bg=BG_COLOR)
    scroll_host.pack(fill="both", expand=True, padx=24, pady=(0, 20))

    hero = tk.Frame(content, bg=CARD_COLOR, padx=22, pady=22)
    hero.pack(fill="x", pady=(0, 18))
    hero.grid_columnconfigure(1, weight=1)

    poster = build_poster_widget(hero, movie, variant="detail", bg=CARD_COLOR)
    poster.grid(row=0, column=0, sticky="nw", padx=(0, 18))

    details = tk.Frame(hero, bg=CARD_COLOR)
    details.grid(row=0, column=1, sticky="nsew", padx=(0, 18))

    build_badge(details, "Watch Online", bg=ACCENT_SOFT, fg=ACCENT_COLOR).pack(anchor="w")
    tk.Label(
        details,
        text=movie["title"],
        bg=CARD_COLOR,
        fg=TEXT_PRIMARY,
        font=TITLE_FONT,
    ).pack(anchor="w", pady=(14, 6))
    tk.Label(
        details,
        text=movie["tagline"],
        bg=CARD_COLOR,
        fg=TEXT_SECONDARY,
        font=BODY_FONT,
        wraplength=560,
        justify="left",
    ).pack(anchor="w")

    meta = tk.Frame(details, bg=CARD_COLOR)
    meta.pack(anchor="w", pady=(16, 14))
    build_badge(meta, f"{movie['year']}", bg=CARD_ALT_COLOR, fg=TEXT_PRIMARY).pack(
        side="left", padx=(0, 8)
    )
    build_badge(meta, movie["genre"], bg=CARD_ALT_COLOR, fg=TEXT_PRIMARY).pack(
        side="left", padx=(0, 8)
    )
    build_badge(meta, movie["language"], bg=CARD_ALT_COLOR, fg=TEXT_PRIMARY).pack(
        side="left", padx=(0, 8)
    )
    build_badge(
        meta,
        f"Rating {movie['rating']:.1f}/10",
        bg=SUCCESS_COLOR,
        fg=BG_COLOR,
    ).pack(side="left")

    if mood:
        tk.Label(
            details,
            text=f"Recommended because you picked a {mood['label'].lower()} mood.",
            bg=CARD_COLOR,
            fg=ACCENT_COLOR,
            font=SMALL_FONT,
        ).pack(anchor="w", pady=(0, 10))

    tk.Label(
        details,
        text=movie["synopsis"],
        bg=CARD_COLOR,
        fg=TEXT_SECONDARY,
        font=BODY_FONT,
        wraplength=560,
        justify="left",
    ).pack(anchor="w")
    tk.Label(
        details,
        text=(
            "The app opens search pages for major streaming services so you can check the "
            "latest availability quickly without broken hardcoded links."
        ),
        bg=CARD_COLOR,
        fg=TEXT_MUTED,
        font=SMALL_FONT,
        wraplength=560,
        justify="left",
    ).pack(anchor="w", pady=(14, 0))

    action_rail = tk.Frame(hero, bg=CARD_ALT_COLOR, padx=16, pady=16)
    action_rail.grid(row=0, column=2, sticky="ne")
    build_badge(action_rail, "Open Fast", bg=ACCENT_SOFT, fg=ACCENT_COLOR).pack(anchor="w")
    tk.Label(
        action_rail,
        text="All actions stay in one clean column.",
        bg=CARD_ALT_COLOR,
        fg=TEXT_MUTED,
        font=SMALL_FONT,
        wraplength=180,
        justify="left",
    ).pack(anchor="w", pady=(10, 14))
    build_primary_button(
        action_rail,
        "Best Option",
        command=lambda: quick_open(movie_id),
        width=16,
    ).pack(anchor="w", pady=(0, 10))
    build_secondary_button(
        action_rail,
        "Trailer First",
        command=lambda: open_trailer(links),
        width=16,
    ).pack(anchor="w", pady=(0, 10))
    build_secondary_button(
        action_rail,
        "Try Another Mood",
        command=lambda: back_to_moods(root),
        width=16,
    ).pack(anchor="w")

    section_header = tk.Frame(content, bg=BG_COLOR)
    section_header.pack(fill="x", pady=(0, 10))
    tk.Label(
        section_header,
        text="Where To Search",
        bg=BG_COLOR,
        fg=TEXT_PRIMARY,
        font=HEADING_FONT,
    ).pack(side="left")
    tk.Label(
        section_header,
        text="Link details on the left, open button on the right",
        bg=BG_COLOR,
        fg=TEXT_MUTED,
        font=SMALL_FONT,
    ).pack(side="right")

    for link in links:
        open_target = lambda selected_url=link["url"]: launch_link(selected_url)

        card = tk.Frame(content, bg=CARD_COLOR, padx=18, pady=18)
        card.pack(fill="x", pady=8)
        card.grid_columnconfigure(0, weight=1)

        details = tk.Frame(card, bg=CARD_COLOR)
        details.grid(row=0, column=0, sticky="nsew", padx=(0, 18))

        build_badge(details, link["platform_name"], bg=ACCENT_SOFT, fg=ACCENT_COLOR).pack(
            anchor="w"
        )
        tk.Label(
            details,
            text=link["action_label"],
            bg=CARD_COLOR,
            fg=TEXT_PRIMARY,
            font=HEADING_FONT,
        ).pack(anchor="w", pady=(10, 6))
        tk.Label(
            details,
            text=get_link_description(link["link_type"]),
            bg=CARD_COLOR,
            fg=TEXT_SECONDARY,
            font=BODY_FONT,
            wraplength=620,
            justify="left",
        ).pack(anchor="w")

        actions = tk.Frame(card, bg=CARD_ALT_COLOR, padx=14, pady=14)
        actions.grid(row=0, column=1, sticky="ne")
        build_primary_button(actions, "Open In Browser", command=open_target, width=16).pack(
            anchor="w"
        )

        make_widget_clickable(card, open_target)
        make_descendants_clickable(details, open_target, skip_classes={"Button", "Entry"})


def get_link_description(link_type):
    if link_type == "trailer":
        return "Preview the movie first with a trailer search before choosing where to stream it."
    return "Search this platform in your browser and check the latest watch-online availability for the movie."


def quick_open(movie_id):
    success, _link = open_primary_link(movie_id)
    if not success:
        messagebox.showwarning("No Link Found", "No streaming links are available for this movie.")


def open_trailer(links):
    for link in links:
        if link["link_type"] == "trailer":
            open_link(link["url"])
            return

    messagebox.showwarning("Trailer Missing", "Trailer link is not available for this movie.")


def launch_link(url):
    open_link(url)


def go_back(root, mood_key):
    if mood_key:
        from show_screen import show_recommendations

        show_recommendations(root, mood_key)
        return

    back_to_moods(root)


def back_to_moods(root):
    from movie_screen import show_movies

    show_movies(root)
