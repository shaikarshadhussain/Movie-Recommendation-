# MoodStream Movie Recommendation App

MoodStream is a mood-based movie recommendation project that now includes:

- a desktop app built with Tkinter
- a Vercel-hosted web version for easy sharing

## Live Demo

Production URL: https://moodstream-movie-recommendation.vercel.app

## What This Project Does

- lets the user choose a mood such as `Happy`, `Romantic`, `Chill`, or `Intense`
- finds movies tagged with that mood
- ranks the matching movies and shows the strongest recommendation first
- shows extra matching titles from the same catalog
- displays local poster assets for each movie
- opens search links for Prime Video, Netflix, Disney+ Hotstar, and YouTube trailers

## What Algorithm Is Used

This project does not use a trained machine learning model. It uses a rule-based recommendation algorithm.

How it works:

1. Each movie in the catalog is assigned one or more mood tags.
2. When the user selects a mood, the app filters the catalog to movies containing that mood tag.
3. Matching movies are sorted by:
   `rating` descending, then `year` descending, then `title` ascending.
4. The highest-ranked result becomes the main recommendation, and the rest are shown as additional matches.

Why this approach was used:

- it is fast and deterministic
- it is easy to explain and debug
- it works well for a curated movie catalog
- it fits both the desktop app and the deployed web version without requiring model hosting

## Tech Stack

- Python 3
- Tkinter for the desktop UI
- HTML, CSS, and JavaScript for the deployed web UI
- Vercel for hosting

## Project Versions

### Desktop App

Run the original desktop version with:

```bash
python main.py
```

### Web App

The Vercel-ready web version uses these files:

- `index.html`
- `styles.css`
- `app.js`
- `assets/data/catalog.json`

## Main Files

- `main.py` - desktop app entry point
- `database.py` - mood data, movie catalog, and ranking source
- `movie_screen.py` - desktop mood picker screen
- `show_screen.py` - desktop recommendation screen
- `seat_screen.py` - desktop watch options screen
- `booking.py` - browser link helpers
- `poster_utils.py` - poster loading helpers
- `theme.py` - desktop UI theme helpers
- `index.html` - deployed web app shell
- `app.js` - web recommendation logic and rendering
- `styles.css` - web styling
- `assets/posters/` - movie poster images
- `assets/data/catalog.json` - shared web catalog data

## Refresh Demo Data

Run any of these scripts if you want to rebuild the local sample catalog:

```bash
python insert_movies.py
python insert_shows.py
python insert_seats.py
```

## Refresh Posters

Fetch real movie posters from TMDB:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\download_real_posters.ps1
```

Rebuild the fallback generated posters instead:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\generate_posters.ps1
```

## Deployment Notes

- deployed to Vercel on the linked project `moodstream-movie-recommendation`
- production alias: https://moodstream-movie-recommendation.vercel.app
- the original Tkinter desktop UI is kept in the repository, but the hosted version is the web frontend because Vercel does not run desktop GUI windows
