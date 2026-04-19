import tkinter as tk

from booking import open_primary_link
from database import get_all_movies, get_mood_option, get_movies_for_mood
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


MOOD_REASON = {
    "happy": "You wanted something uplifting, so the top suggestion leans bright, watchable, and easy to enjoy.",
    "romantic": "You picked romance, so this lead recommendation gives you chemistry, warmth, and emotional payoff first.",
    "adventurous": "You asked for movement and scale, so this first pick is all about momentum and escape.",
    "thoughtful": "You chose a reflective mood, so the top match gives you atmosphere, ideas, and something to sit with.",
    "intense": "You picked high energy, so the recommendation starts with the strongest pressure and cinematic drive.",
    "nostalgic": "You wanted comfort and memory, so this first pick leans warm, familiar, and rewatchable.",
    "emotional": "You picked emotion, so the recommendation opens with the movie most likely to stay with you.",
    "chill": "You wanted a softer watch, so the first pick keeps the night easy, cozy, and low-stress.",
}


def show_recommendations(root, mood_key):
    clear_screen(root)

    mood = get_mood_option(mood_key)
    movies = get_movies_for_mood(mood_key)
    if not movies:
        movies = get_all_movies()

    mood_label = mood["label"] if mood else "Your"
    root.title(f"{mood_label} Picks | MoodStream")

    page = tk.Frame(root, bg=BG_COLOR)
    page.pack(fill="both", expand=True)

    top_bar = tk.Frame(page, bg=BG_COLOR)
    top_bar.pack(fill="x", padx=24, pady=(18, 10))

    build_secondary_button(top_bar, "Back To Moods", command=lambda: go_back(root), width=16).pack(
        side="left"
    )
    tk.Label(
        top_bar,
        text="Recommendation details on the left, action rail on the right",
        bg=BG_COLOR,
        fg=TEXT_MUTED,
        font=SMALL_FONT,
    ).pack(side="right")

    scroll_host, content = build_scrollable_content(page, bg=BG_COLOR)
    scroll_host.pack(fill="both", expand=True, padx=24, pady=(0, 20))

    if not movies:
        tk.Label(
            content,
            text="No recommendations are available right now.",
            bg=BG_COLOR,
            fg=TEXT_SECONDARY,
            font=BODY_FONT,
        ).pack(anchor="w")
        return

    featured_movie = movies[0]
    secondary_movies = movies[1:7]

    hero = tk.Frame(content, bg=CARD_COLOR, padx=22, pady=22)
    hero.pack(fill="x", pady=(0, 18))
    hero.grid_columnconfigure(1, weight=1)

    poster = build_poster_widget(hero, featured_movie, variant="detail", bg=CARD_COLOR)
    poster.grid(row=0, column=0, sticky="nw", padx=(0, 18))

    details = tk.Frame(hero, bg=CARD_COLOR)
    details.grid(row=0, column=1, sticky="nsew", padx=(0, 18))

    build_badge(details, f"{mood_label} Match", bg=ACCENT_SOFT, fg=ACCENT_COLOR).pack(anchor="w")
    tk.Label(
        details,
        text=featured_movie["title"],
        bg=CARD_COLOR,
        fg=TEXT_PRIMARY,
        font=TITLE_FONT,
    ).pack(anchor="w", pady=(14, 6))
    tk.Label(
        details,
        text=featured_movie["tagline"],
        bg=CARD_COLOR,
        fg=TEXT_SECONDARY,
        font=BODY_FONT,
        wraplength=560,
        justify="left",
    ).pack(anchor="w")
    tk.Label(
        details,
        text=MOOD_REASON.get(
            mood_key, "This one rose to the top as the strongest overall match from the catalog."
        ),
        bg=CARD_COLOR,
        fg=TEXT_MUTED,
        font=SMALL_FONT,
        wraplength=560,
        justify="left",
    ).pack(anchor="w", pady=(12, 14))

    meta = tk.Frame(details, bg=CARD_COLOR)
    meta.pack(anchor="w", pady=(0, 14))
    build_badge(meta, f"{featured_movie['year']}", bg=CARD_ALT_COLOR, fg=TEXT_PRIMARY).pack(
        side="left", padx=(0, 8)
    )
    build_badge(meta, featured_movie["genre"], bg=CARD_ALT_COLOR, fg=TEXT_PRIMARY).pack(
        side="left", padx=(0, 8)
    )
    build_badge(
        meta,
        f"{featured_movie['language']}  |  {featured_movie['duration']} min",
        bg=CARD_ALT_COLOR,
        fg=TEXT_PRIMARY,
    ).pack(side="left", padx=(0, 8))
    build_badge(
        meta,
        f"Rating {featured_movie['rating']:.1f}/10",
        bg=CARD_ALT_COLOR,
        fg=TEXT_PRIMARY,
    ).pack(side="left")

    tk.Label(
        details,
        text=featured_movie["synopsis"],
        bg=CARD_COLOR,
        fg=TEXT_SECONDARY,
        font=BODY_FONT,
        wraplength=560,
        justify="left",
    ).pack(anchor="w")

    mood_tags = tk.Frame(details, bg=CARD_COLOR)
    mood_tags.pack(anchor="w", pady=(16, 0))
    for mood_tag in featured_movie["moods"]:
        build_badge(mood_tags, mood_tag.title(), bg=CARD_ALT_COLOR, fg=TEXT_PRIMARY).pack(
            side="left", padx=(0, 8)
        )

    actions = tk.Frame(hero, bg=CARD_ALT_COLOR, padx=16, pady=16)
    actions.grid(row=0, column=2, sticky="ne")
    build_badge(actions, "Watch Next", bg=ACCENT_SOFT, fg=ACCENT_COLOR).pack(anchor="w")
    tk.Label(
        actions,
        text="Every major action stays grouped here.",
        bg=CARD_ALT_COLOR,
        fg=TEXT_MUTED,
        font=SMALL_FONT,
        wraplength=180,
        justify="left",
    ).pack(anchor="w", pady=(10, 14))
    build_primary_button(
        actions,
        "Watch Online",
        command=lambda: open_watch_options(root, featured_movie["movie_id"], mood_key),
        width=16,
    ).pack(anchor="w", pady=(0, 10))
    build_secondary_button(
        actions,
        "Quick Open",
        command=lambda: open_primary_link(featured_movie["movie_id"]),
        width=16,
    ).pack(anchor="w", pady=(0, 10))
    build_secondary_button(
        actions,
        "Pick Another Mood",
        command=lambda: go_back(root),
        width=16,
    ).pack(anchor="w")

    section_header = tk.Frame(content, bg=BG_COLOR)
    section_header.pack(fill="x", pady=(0, 10))
    tk.Label(
        section_header,
        text=f"More {mood_label} Recommendations",
        bg=BG_COLOR,
        fg=TEXT_PRIMARY,
        font=HEADING_FONT,
    ).pack(side="left")
    tk.Label(
        section_header,
        text="Same poster-plus-actions layout for every card",
        bg=BG_COLOR,
        fg=TEXT_MUTED,
        font=SMALL_FONT,
    ).pack(side="right")

    if not secondary_movies:
        tk.Label(
            content,
            text="The catalog has one perfect match for this mood right now.",
            bg=BG_COLOR,
            fg=TEXT_SECONDARY,
            font=BODY_FONT,
        ).pack(anchor="w")
        return

    for movie in secondary_movies:
        open_movie = lambda selected_id=movie["movie_id"]: open_watch_options(
            root, selected_id, mood_key
        )

        card = tk.Frame(content, bg=CARD_COLOR, padx=18, pady=18)
        card.pack(fill="x", pady=8)
        card.grid_columnconfigure(1, weight=1)

        poster_frame = build_poster_widget(card, movie, variant="featured", bg=CARD_COLOR)
        poster_frame.grid(row=0, column=0, sticky="nw", padx=(0, 18))

        details = tk.Frame(card, bg=CARD_COLOR)
        details.grid(row=0, column=1, sticky="nsew", padx=(0, 18))

        tk.Label(
            details,
            text=movie["title"],
            bg=CARD_COLOR,
            fg=TEXT_PRIMARY,
            font=HEADING_FONT,
        ).pack(anchor="w")
        tk.Label(
            details,
            text=f"{movie['year']}  |  {movie['genre']}  |  Rating {movie['rating']:.1f}/10",
            bg=CARD_COLOR,
            fg=TEXT_SECONDARY,
            font=BODY_FONT,
        ).pack(anchor="w", pady=(6, 6))
        tk.Label(
            details,
            text=movie["tagline"],
            bg=CARD_COLOR,
            fg=TEXT_MUTED,
            font=SMALL_FONT,
            wraplength=560,
            justify="left",
        ).pack(anchor="w")
        tk.Label(
            details,
            text=movie["synopsis"],
            bg=CARD_COLOR,
            fg=TEXT_SECONDARY,
            font=BODY_FONT,
            wraplength=560,
            justify="left",
        ).pack(anchor="w", pady=(10, 0))

        tag_row = tk.Frame(details, bg=CARD_COLOR)
        tag_row.pack(anchor="w", pady=(12, 0))
        for mood_tag in movie["moods"][:3]:
            build_badge(tag_row, mood_tag.title(), bg=CARD_ALT_COLOR, fg=TEXT_PRIMARY).pack(
                side="left", padx=(0, 8)
            )

        action_rail = tk.Frame(card, bg=CARD_ALT_COLOR, padx=14, pady=14)
        action_rail.grid(row=0, column=2, sticky="ne")
        build_primary_button(action_rail, "Watch Online", command=open_movie, width=15).pack(
            anchor="w", pady=(0, 10)
        )
        build_secondary_button(
            action_rail,
            "Quick Open",
            command=lambda selected_id=movie["movie_id"]: open_primary_link(selected_id),
            width=15,
        ).pack(anchor="w")

        make_widget_clickable(card, open_movie)
        make_widget_clickable(poster_frame, open_movie)
        make_descendants_clickable(poster_frame, open_movie, skip_classes={"Button", "Entry"})
        make_descendants_clickable(details, open_movie, skip_classes={"Button", "Entry"})


def open_watch_options(root, movie_id, mood_key=None):
    from seat_screen import show_watch_options

    show_watch_options(root, movie_id, mood_key)


def go_back(root):
    from movie_screen import show_movies

    show_movies(root)
