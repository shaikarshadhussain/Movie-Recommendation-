import random
import tkinter as tk

from database import get_featured_movies, get_mood_options
from poster_utils import build_poster_widget
from theme import (
    ACCENT_COLOR,
    ACCENT_SOFT,
    BG_COLOR,
    BODY_FONT,
    CARD_ALT_COLOR,
    CARD_COLOR,
    HEADING_FONT,
    HERO_FONT,
    SMALL_FONT,
    SUCCESS_COLOR,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TITLE_FONT,
    attach_hover,
    build_badge,
    build_primary_button,
    build_scrollable_content,
    build_secondary_button,
    clear_screen,
    make_descendants_clickable,
    make_widget_clickable,
)


def show_movies(root):
    clear_screen(root)
    root.title("MoodStream | Movie Recommendation")

    moods = get_mood_options()
    featured_movies = get_featured_movies(limit=7)
    top_pick = featured_movies[0]
    trending_movies = featured_movies[1:] if len(featured_movies) > 1 else featured_movies
    open_top_pick = lambda: open_watch_options(root, top_pick["movie_id"])

    page = tk.Frame(root, bg=BG_COLOR)
    page.pack(fill="both", expand=True)

    scroll_host, content = build_scrollable_content(page, bg=BG_COLOR)
    scroll_host.pack(fill="both", expand=True, padx=24, pady=18)

    nav = tk.Frame(content, bg=BG_COLOR)
    nav.pack(fill="x", pady=(0, 18))

    brand = tk.Frame(nav, bg=BG_COLOR)
    brand.pack(side="left")
    tk.Label(
        brand,
        text="MOODSTREAM",
        bg=BG_COLOR,
        fg=ACCENT_COLOR,
        font=("Bahnschrift SemiBold", 20),
    ).pack(anchor="w")
    tk.Label(
        brand,
        text="Pick a mood, get a recommendation, and jump into watch options from one polished flow.",
        bg=BG_COLOR,
        fg=TEXT_MUTED,
        font=SMALL_FONT,
    ).pack(anchor="w", pady=(4, 0))

    nav_actions = tk.Frame(nav, bg=BG_COLOR)
    nav_actions.pack(side="right")
    build_secondary_button(
        nav_actions,
        "Romantic Night",
        command=lambda: open_recommendations(root, "romantic"),
        width=16,
    ).pack(side="left", padx=(0, 10))
    build_primary_button(
        nav_actions,
        "Surprise Me",
        command=lambda: open_recommendations(root, random.choice(moods)["key"]),
        width=14,
    ).pack(side="left")

    hero = tk.Frame(content, bg=CARD_COLOR, padx=28, pady=28)
    hero.pack(fill="x", pady=(0, 22))

    hero_body = tk.Frame(hero, bg=CARD_COLOR)
    hero_body.pack(fill="x")
    hero_body.grid_columnconfigure(0, weight=1)

    content_side = tk.Frame(hero_body, bg=CARD_COLOR)
    content_side.grid(row=0, column=0, sticky="nsew", padx=(0, 18))

    build_badge(content_side, "Prime-inspired movie night", bg=ACCENT_SOFT, fg=ACCENT_COLOR).pack(
        anchor="w"
    )
    tk.Label(
        content_side,
        text="Mood-first recommendations with posters, cleaner layout, and faster watch access.",
        bg=CARD_COLOR,
        fg=TEXT_PRIMARY,
        font=HERO_FONT,
        wraplength=610,
        justify="left",
    ).pack(anchor="w", pady=(16, 10))
    tk.Label(
        content_side,
        text=(
            "Start by choosing your mood below, or jump straight into our top recommendation "
            f"right now: {top_pick['title']}."
        ),
        bg=CARD_COLOR,
        fg=TEXT_SECONDARY,
        font=BODY_FONT,
        wraplength=610,
        justify="left",
    ).pack(anchor="w")

    badges = tk.Frame(content_side, bg=CARD_COLOR)
    badges.pack(anchor="w", pady=(18, 0))
    build_badge(badges, f"{len(moods)} moods", bg=CARD_ALT_COLOR, fg=TEXT_PRIMARY).pack(
        side="left", padx=(0, 10)
    )
    build_badge(
        badges,
        f"{len(featured_movies)} spotlight titles",
        bg=CARD_ALT_COLOR,
        fg=TEXT_PRIMARY,
    ).pack(side="left", padx=(0, 10))
    build_badge(badges, "Poster-based layout", bg=SUCCESS_COLOR, fg=BG_COLOR).pack(side="left")

    spotlight = tk.Frame(content_side, bg=CARD_ALT_COLOR, padx=16, pady=14)
    spotlight.pack(anchor="w", fill="x", pady=(20, 0))
    tk.Label(
        spotlight,
        text="Tonight's spotlight",
        bg=CARD_ALT_COLOR,
        fg=ACCENT_COLOR,
        font=SMALL_FONT,
    ).pack(anchor="w")
    tk.Label(
        spotlight,
        text=top_pick["title"],
        bg=CARD_ALT_COLOR,
        fg=TEXT_PRIMARY,
        font=HEADING_FONT,
    ).pack(anchor="w", pady=(6, 4))
    tk.Label(
        spotlight,
        text=top_pick["tagline"],
        bg=CARD_ALT_COLOR,
        fg=TEXT_SECONDARY,
        font=BODY_FONT,
        wraplength=560,
        justify="left",
    ).pack(anchor="w")
    make_widget_clickable(spotlight, open_top_pick)
    make_descendants_clickable(spotlight, open_top_pick, skip_classes={"Button", "Entry"})

    poster_side = tk.Frame(hero_body, bg=CARD_COLOR)
    poster_side.grid(row=0, column=1, sticky="n", padx=(0, 18))
    poster = build_poster_widget(poster_side, top_pick, variant="hero", bg=CARD_COLOR)
    poster.pack(anchor="n")
    make_widget_clickable(poster, open_top_pick)
    make_descendants_clickable(poster, open_top_pick, skip_classes={"Button", "Entry"})

    action_rail = tk.Frame(hero_body, bg=CARD_ALT_COLOR, padx=16, pady=16)
    action_rail.grid(row=0, column=2, sticky="ne")
    build_badge(action_rail, "Quick Actions", bg=ACCENT_SOFT, fg=ACCENT_COLOR).pack(anchor="w")
    tk.Label(
        action_rail,
        text="Keep every action together on one side.",
        bg=CARD_ALT_COLOR,
        fg=TEXT_MUTED,
        font=SMALL_FONT,
        wraplength=180,
        justify="left",
    ).pack(anchor="w", pady=(10, 14))
    build_primary_button(
        action_rail,
        "Watch Top Pick",
        command=lambda: open_watch_options(root, top_pick["movie_id"]),
        width=16,
    ).pack(anchor="w", pady=(0, 10))
    build_secondary_button(
        action_rail,
        "Top Feel-Good",
        command=lambda: open_recommendations(root, "happy"),
        width=16,
    ).pack(anchor="w", pady=(0, 10))
    build_secondary_button(
        action_rail,
        "Adventure Mode",
        command=lambda: open_recommendations(root, "adventurous"),
        width=16,
    ).pack(anchor="w")

    mood_header = tk.Frame(content, bg=BG_COLOR)
    mood_header.pack(fill="x", pady=(0, 10))
    tk.Label(
        mood_header,
        text="Choose Your Mood",
        bg=BG_COLOR,
        fg=TEXT_PRIMARY,
        font=TITLE_FONT,
    ).pack(side="left")
    tk.Label(
        mood_header,
        text="Mood cards open the recommendation screen directly",
        bg=BG_COLOR,
        fg=TEXT_MUTED,
        font=SMALL_FONT,
    ).pack(side="right")

    mood_grid = tk.Frame(content, bg=BG_COLOR)
    mood_grid.pack(fill="x", pady=(0, 22))

    for column_index in range(2):
        mood_grid.grid_columnconfigure(column_index, weight=1)

    for index, mood in enumerate(moods):
        row_index = index // 2
        column_index = index % 2
        open_mood = lambda selected_key=mood["key"]: open_recommendations(root, selected_key)

        card = tk.Frame(mood_grid, bg=CARD_COLOR, padx=18, pady=18)
        card.grid(row=row_index, column=column_index, sticky="nsew", padx=8, pady=8)
        attach_hover(card, CARD_COLOR, CARD_ALT_COLOR)

        build_badge(card, mood["label"], bg=ACCENT_SOFT, fg=ACCENT_COLOR).pack(anchor="w")
        tk.Label(
            card,
            text=f"{mood['label']} night",
            bg=CARD_COLOR,
            fg=TEXT_PRIMARY,
            font=HEADING_FONT,
        ).pack(anchor="w", pady=(12, 6))
        tk.Label(
            card,
            text=mood["description"],
            bg=CARD_COLOR,
            fg=TEXT_SECONDARY,
            font=BODY_FONT,
            wraplength=360,
            justify="left",
        ).pack(anchor="w")
        tk.Label(
            card,
            text="Click anywhere on the card",
            bg=CARD_COLOR,
            fg=TEXT_MUTED,
            font=SMALL_FONT,
        ).pack(anchor="w", pady=(16, 0))

        make_widget_clickable(card, open_mood)
        make_descendants_clickable(card, open_mood, skip_classes={"Button", "Entry"})

    featured_header = tk.Frame(content, bg=BG_COLOR)
    featured_header.pack(fill="x", pady=(0, 10))
    tk.Label(
        featured_header,
        text="Trending Tonight",
        bg=BG_COLOR,
        fg=TEXT_PRIMARY,
        font=TITLE_FONT,
    ).pack(side="left")
    tk.Label(
        featured_header,
        text="Posters on the left, actions on the right",
        bg=BG_COLOR,
        fg=TEXT_MUTED,
        font=SMALL_FONT,
    ).pack(side="right")

    for movie in trending_movies:
        open_movie = lambda selected_id=movie["movie_id"]: open_watch_options(root, selected_id)

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
            text=f"{movie['year']}  |  {movie['genre']}  |  {movie['language']}",
            bg=CARD_COLOR,
            fg=TEXT_SECONDARY,
            font=BODY_FONT,
        ).pack(anchor="w", pady=(6, 8))
        tk.Label(
            details,
            text=movie["tagline"],
            bg=CARD_COLOR,
            fg=TEXT_MUTED,
            font=SMALL_FONT,
            wraplength=560,
            justify="left",
        ).pack(anchor="w")

        meta = tk.Frame(details, bg=CARD_COLOR)
        meta.pack(anchor="w", pady=(12, 0))
        for mood_tag in movie["moods"][:3]:
            build_badge(meta, mood_tag.title(), bg=CARD_ALT_COLOR, fg=TEXT_PRIMARY).pack(
                side="left", padx=(0, 8)
            )

        actions = tk.Frame(card, bg=CARD_ALT_COLOR, padx=14, pady=14)
        actions.grid(row=0, column=2, sticky="ne")
        build_primary_button(actions, "Watch Online", command=open_movie, width=15).pack(
            anchor="w", pady=(0, 10)
        )
        build_secondary_button(
            actions,
            "By Mood",
            command=lambda selected_mood=movie["moods"][0]: open_recommendations(root, selected_mood),
            width=15,
        ).pack(anchor="w")

        make_widget_clickable(card, open_movie)
        make_widget_clickable(poster_frame, open_movie)
        make_descendants_clickable(poster_frame, open_movie, skip_classes={"Button", "Entry"})
        make_descendants_clickable(details, open_movie, skip_classes={"Button", "Entry"})


def open_recommendations(root, mood_key):
    from show_screen import show_recommendations

    show_recommendations(root, mood_key)


def open_watch_options(root, movie_id):
    from seat_screen import show_watch_options

    show_watch_options(root, movie_id)
