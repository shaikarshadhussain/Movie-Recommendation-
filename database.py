from copy import deepcopy
from urllib.parse import quote_plus

MOOD_OPTIONS = [
    {
        "key": "happy",
        "label": "Happy",
        "description": "Bright, easygoing movies that lift the room.",
    },
    {
        "key": "romantic",
        "label": "Romantic",
        "description": "Warm, dreamy stories when you want heart first.",
    },
    {
        "key": "adventurous",
        "label": "Adventurous",
        "description": "Big journeys, momentum, and cinematic escape.",
    },
    {
        "key": "thoughtful",
        "label": "Thoughtful",
        "description": "Smart, reflective movies that stay with you.",
    },
    {
        "key": "intense",
        "label": "Intense",
        "description": "Sharp tension, adrenaline, and edge-of-seat energy.",
    },
    {
        "key": "nostalgic",
        "label": "Nostalgic",
        "description": "Comfort-watch picks with warmth and memory.",
    },
    {
        "key": "emotional",
        "label": "Emotional",
        "description": "Meaningful stories with a deeper emotional pull.",
    },
    {
        "key": "chill",
        "label": "Chill",
        "description": "Relaxed late-night picks that feel cozy and easy.",
    },
]

MOVIE_CATALOG = [
    {
        "title": "Interstellar",
        "year": 2014,
        "genre": "Science Fiction",
        "language": "English",
        "duration": 169,
        "rating": 8.7,
        "moods": ["thoughtful", "intense", "emotional"],
        "tagline": "Big ideas, huge emotion, and spectacle with depth.",
        "synopsis": (
            "A team travels through space in search of humanity's future, balancing "
            "mind-bending science with a deeply emotional core."
        ),
    },
    {
        "title": "Your Name",
        "year": 2016,
        "genre": "Fantasy Romance",
        "language": "Japanese",
        "duration": 106,
        "rating": 8.4,
        "moods": ["romantic", "emotional", "nostalgic"],
        "tagline": "A heartfelt, time-bending story that feels intimate and sweeping.",
        "synopsis": (
            "Two teenagers mysteriously swap lives and begin a search that turns into "
            "one of the most moving modern romance stories."
        ),
    },
    {
        "title": "Coco",
        "year": 2017,
        "genre": "Animation Family",
        "language": "English",
        "duration": 105,
        "rating": 8.4,
        "moods": ["happy", "emotional", "nostalgic"],
        "tagline": "Colorful, musical, and genuinely moving in the best way.",
        "synopsis": (
            "A young musician journeys into the Land of the Dead and uncovers the story "
            "of his family with warmth, joy, and tears."
        ),
    },
    {
        "title": "Soul",
        "year": 2020,
        "genre": "Animation Drama",
        "language": "English",
        "duration": 100,
        "rating": 8.1,
        "moods": ["thoughtful", "chill", "emotional"],
        "tagline": "A warm, soulful reminder to enjoy being alive.",
        "synopsis": (
            "A musician on the edge of his breakthrough gets a cosmic detour that turns "
            "into a reflective and unexpectedly gentle story about life."
        ),
    },
    {
        "title": "Zindagi Na Milegi Dobara",
        "year": 2011,
        "genre": "Comedy Drama",
        "language": "Hindi",
        "duration": 155,
        "rating": 8.2,
        "moods": ["happy", "adventurous", "chill"],
        "tagline": "Friendship, travel, and a reminder to live a little louder.",
        "synopsis": (
            "Three friends head out on a road trip that slowly becomes a reset button "
            "for fear, friendship, and joy."
        ),
    },
    {
        "title": "Mad Max: Fury Road",
        "year": 2015,
        "genre": "Action Adventure",
        "language": "English",
        "duration": 120,
        "rating": 8.1,
        "moods": ["intense", "adventurous"],
        "tagline": "Pure velocity, world-class action, and relentless momentum.",
        "synopsis": (
            "A brutal chase across a desert wasteland turns into a masterclass in visual "
            "storytelling and adrenaline."
        ),
    },
    {
        "title": "Queen",
        "year": 2013,
        "genre": "Comedy Drama",
        "language": "Hindi",
        "duration": 146,
        "rating": 8.1,
        "moods": ["happy", "adventurous", "emotional"],
        "tagline": "A solo trip becomes a joyful story of self-discovery.",
        "synopsis": (
            "After a sudden heartbreak, a young woman takes herself on the honeymoon she "
            "was meant to share and finds a whole new version of herself."
        ),
    },
    {
        "title": "About Time",
        "year": 2013,
        "genre": "Romance Drama",
        "language": "English",
        "duration": 123,
        "rating": 7.8,
        "moods": ["romantic", "chill", "emotional"],
        "tagline": "Love, family, and time travel with an incredibly soft heart.",
        "synopsis": (
            "A young man learns he can travel through time and slowly realizes the real "
            "magic is in ordinary days and the people he loves."
        ),
    },
    {
        "title": "Spider-Man: Into the Spider-Verse",
        "year": 2018,
        "genre": "Animation Action",
        "language": "English",
        "duration": 117,
        "rating": 8.4,
        "moods": ["happy", "adventurous", "intense"],
        "tagline": "Stylish, electric, and full of momentum and heart.",
        "synopsis": (
            "Miles Morales steps into the multiverse and becomes the center of one of the "
            "most inventive and fun superhero stories around."
        ),
    },
    {
        "title": "La La Land",
        "year": 2016,
        "genre": "Romance Musical",
        "language": "English",
        "duration": 128,
        "rating": 8.0,
        "moods": ["romantic", "emotional", "nostalgic"],
        "tagline": "A stylish love story full of color, music, and ache.",
        "synopsis": (
            "Two dreamers fall in love while chasing their ambitions, creating a movie "
            "that feels dazzling and bittersweet at the same time."
        ),
    },
    {
        "title": "The Martian",
        "year": 2015,
        "genre": "Science Fiction",
        "language": "English",
        "duration": 144,
        "rating": 8.0,
        "moods": ["happy", "adventurous", "thoughtful"],
        "tagline": "A survival story powered by wit, grit, and optimism.",
        "synopsis": (
            "An astronaut stranded on Mars uses science, humor, and stubborn resilience "
            "to survive while the world figures out how to bring him home."
        ),
    },
    {
        "title": "3 Idiots",
        "year": 2009,
        "genre": "Comedy Drama",
        "language": "Hindi",
        "duration": 170,
        "rating": 8.4,
        "moods": ["happy", "thoughtful", "emotional"],
        "tagline": "Funny, moving, and surprisingly sharp about life choices.",
        "synopsis": (
            "Three engineering students learn that success means a lot more than marks, "
            "status, or simply following the path everyone expects."
        ),
    },
    {
        "title": "The Grand Budapest Hotel",
        "year": 2014,
        "genre": "Comedy Adventure",
        "language": "English",
        "duration": 99,
        "rating": 8.1,
        "moods": ["chill", "nostalgic", "happy"],
        "tagline": "Precise, playful, and beautifully odd in the best way.",
        "synopsis": (
            "A meticulous concierge and his lobby boy move through a whimsical old-world "
            "mystery full of style, comedy, and charm."
        ),
    },
    {
        "title": "Little Miss Sunshine",
        "year": 2006,
        "genre": "Comedy Drama",
        "language": "English",
        "duration": 101,
        "rating": 7.8,
        "moods": ["happy", "nostalgic", "emotional"],
        "tagline": "Messy family chaos that somehow turns deeply comforting.",
        "synopsis": (
            "A wildly imperfect family piles into a van for a road trip that becomes "
            "funny, tender, and unexpectedly life-affirming."
        ),
    },
    {
        "title": "Whiplash",
        "year": 2014,
        "genre": "Drama Music",
        "language": "English",
        "duration": 106,
        "rating": 8.5,
        "moods": ["intense", "thoughtful", "emotional"],
        "tagline": "Pressure, obsession, and rhythm pushed to the limit.",
        "synopsis": (
            "A driven drummer and a brutal instructor collide in a tense, blistering story "
            "about ambition, talent, and the cost of greatness."
        ),
    },
    {
        "title": "Jab We Met",
        "year": 2007,
        "genre": "Romance Comedy",
        "language": "Hindi",
        "duration": 138,
        "rating": 7.9,
        "moods": ["romantic", "happy", "chill"],
        "tagline": "A runaway train of charm, comfort, and chemistry.",
        "synopsis": (
            "A chance journey throws together a free-spirited woman and a lost businessman "
            "in one of Hindi cinema's most rewatchable romances."
        ),
    },
    {
        "title": "Wake Up Sid",
        "year": 2009,
        "genre": "Coming-of-Age Drama",
        "language": "Hindi",
        "duration": 138,
        "rating": 7.6,
        "moods": ["chill", "thoughtful", "nostalgic"],
        "tagline": "A soft, city-lit comfort watch about growing up slowly.",
        "synopsis": (
            "A drifting college graduate learns how to take life seriously without losing "
            "the warmth and softness that make him who he is."
        ),
    },
    {
        "title": "The Secret Life of Walter Mitty",
        "year": 2013,
        "genre": "Adventure Drama",
        "language": "English",
        "duration": 114,
        "rating": 7.3,
        "moods": ["happy", "adventurous", "thoughtful"],
        "tagline": "A quiet life opens into a globe-spanning reset.",
        "synopsis": (
            "A daydreaming photo editor is pushed out of routine and into a real-world "
            "adventure that feels equal parts inspiring and comforting."
        ),
    },
    {
        "title": "The Intern",
        "year": 2015,
        "genre": "Comedy Drama",
        "language": "English",
        "duration": 121,
        "rating": 7.1,
        "moods": ["chill", "happy", "thoughtful"],
        "tagline": "Soft energy, easy humor, and quietly comforting chemistry.",
        "synopsis": (
            "A retired widower joins an online fashion company and ends up becoming the "
            "steady heart of the story."
        ),
    },
]

STREAMING_PLATFORMS = (
    ("Prime Video", "Search Prime Video"),
    ("Netflix", "Search Netflix"),
    ("Disney+ Hotstar", "Search Hotstar"),
)

_MOVIES = []
_PLATFORM_LINKS = {}


def create_database():
    seed_demo_data()


def seed_demo_data(force_refresh=False):
    global _MOVIES, _PLATFORM_LINKS

    if _MOVIES and not force_refresh:
        return

    _MOVIES = []
    _PLATFORM_LINKS = {}

    for movie_id, movie in enumerate(MOVIE_CATALOG, start=1):
        movie_record = deepcopy(movie)
        movie_record["movie_id"] = movie_id
        _MOVIES.append(movie_record)
        _PLATFORM_LINKS[movie_id] = build_platform_rows(movie_id, movie["title"])

    _MOVIES.sort(key=lambda movie: (-movie["rating"], movie["title"]))


def build_platform_rows(movie_id, title):
    rows = []
    for link_id, (platform_name, action_label) in enumerate(STREAMING_PLATFORMS, start=1):
        query = quote_plus(f"{title} {platform_name} watch online")
        rows.append(
            {
                "link_id": link_id,
                "movie_id": movie_id,
                "platform_name": platform_name,
                "action_label": action_label,
                "url": f"https://www.google.com/search?q={query}",
                "link_type": "streaming_search",
            }
        )

    trailer_query = quote_plus(f"{title} official trailer")
    rows.append(
        {
            "link_id": len(rows) + 1,
            "movie_id": movie_id,
            "platform_name": "YouTube",
            "action_label": "Watch Trailer",
            "url": f"https://www.youtube.com/results?search_query={trailer_query}",
            "link_type": "trailer",
        }
    )
    return rows


def get_mood_options():
    return deepcopy(MOOD_OPTIONS)


def get_mood_option(mood_key):
    for mood in MOOD_OPTIONS:
        if mood["key"] == mood_key:
            return deepcopy(mood)
    return None


def get_all_movies():
    seed_demo_data()
    return deepcopy(_MOVIES)


def get_featured_movies(limit=4):
    return get_all_movies()[:limit]


def get_movies_for_mood(mood_key):
    seed_demo_data()
    movies = [movie for movie in _MOVIES if mood_key in movie["moods"]]
    movies.sort(key=lambda movie: (-movie["rating"], -movie["year"], movie["title"]))
    return deepcopy(movies)


def get_movie(movie_id):
    seed_demo_data()
    for movie in _MOVIES:
        if movie["movie_id"] == movie_id:
            return deepcopy(movie)
    return None


def get_platform_links(movie_id):
    seed_demo_data()
    return deepcopy(_PLATFORM_LINKS.get(movie_id, []))
