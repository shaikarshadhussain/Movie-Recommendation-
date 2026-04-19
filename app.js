const state = {
  catalog: null,
  activeMood: null,
};

const moodGrid = document.getElementById("mood-grid");
const spotlightCard = document.getElementById("spotlight-card");
const featuredResult = document.getElementById("featured-result");
const matchList = document.getElementById("match-list");
const selectionCopy = document.getElementById("selection-copy");
const surpriseButton = document.getElementById("surprise-button");
const moodCount = document.getElementById("mood-count");
const movieCount = document.getElementById("movie-count");

const moodReason = {
  happy:
    "You wanted something uplifting, so the first result leans bright, easy to watch, and reliably energizing.",
  romantic:
    "You picked romance, so the top suggestion prioritizes warmth, chemistry, and emotional payoff.",
  adventurous:
    "You asked for movement and escape, so the highest-ranked movie leads with momentum and scale.",
  thoughtful:
    "You chose a reflective night, so the recommendation favors atmosphere, ideas, and staying power.",
  intense:
    "You picked high energy, so the first movie pushes the strongest tension and cinematic drive.",
  nostalgic:
    "You wanted comfort and memory, so the leading title feels warm, familiar, and rewatchable.",
  emotional:
    "You asked for emotional impact, so the first result is the one most likely to linger after the credits.",
  chill:
    "You wanted an easygoing watch, so the ranking starts with the softest and coziest fit.",
};

async function init() {
  const response = await fetch("assets/data/catalog.json");
  const catalog = await response.json();

  state.catalog = catalog;
  state.catalog.movies = catalog.movies
    .slice()
    .sort((left, right) => right.rating - left.rating || left.title.localeCompare(right.title));

  moodCount.textContent = String(catalog.moods.length);
  movieCount.textContent = String(catalog.movies.length);

  renderMoods();
  renderSpotlight();
  selectMood("happy");

  surpriseButton.addEventListener("click", () => {
    const moods = state.catalog.moods;
    const randomMood = moods[Math.floor(Math.random() * moods.length)];
    selectMood(randomMood.key);
  });
}

function renderMoods() {
  moodGrid.innerHTML = "";

  state.catalog.moods.forEach((mood) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "mood-card";
    button.innerHTML = `
      <p class="selection-badge">${mood.label}</p>
      <h3>${mood.label} night</h3>
      <p>${mood.description}</p>
    `;
    button.addEventListener("click", () => selectMood(mood.key));
    moodGrid.appendChild(button);
  });
}

function renderSpotlight() {
  const topMovie = state.catalog.movies[0];
  spotlightCard.innerHTML = buildMovieMarkup(topMovie, {
    compact: true,
    badge: "Highest rated catalog pick",
    description:
      "This spotlight uses the full catalog ranking and gives visitors a quick feel for the project before they choose a mood.",
  });
}

function selectMood(moodKey) {
  state.activeMood = moodKey;

  [...moodGrid.children].forEach((card, index) => {
    card.classList.toggle("active", state.catalog.moods[index].key === moodKey);
  });

  const mood = state.catalog.moods.find((item) => item.key === moodKey);
  const matches = getMoviesForMood(moodKey);
  const featuredMovie = matches[0];
  const supportingMovies = matches.slice(1, 7);

  selectionCopy.textContent = `${mood.label} mode is active. Movies are filtered by mood tag, then ranked by rating, year, and title.`;
  featuredResult.innerHTML = buildMovieMarkup(featuredMovie, {
    badge: `${mood.label} best match`,
    description: moodReason[moodKey],
  });

  matchList.innerHTML = "";
  supportingMovies.forEach((movie) => {
    const card = document.createElement("article");
    card.className = "match-card";
    card.innerHTML = buildMovieMarkup(movie, {
      compact: true,
      badge: "Next best fit",
      description: movie.synopsis,
    });
    matchList.appendChild(card);
  });
}

function getMoviesForMood(moodKey) {
  return state.catalog.movies
    .filter((movie) => movie.moods.includes(moodKey))
    .slice()
    .sort(
      (left, right) =>
        right.rating - left.rating ||
        right.year - left.year ||
        left.title.localeCompare(right.title),
    );
}

function buildMovieMarkup(movie, options = {}) {
  const { compact = false, badge = "Top pick", description = "" } = options;
  const wrapperClass = compact ? "match-layout" : "featured-layout";
  const copyClass = compact ? "match-copy" : "featured-copy";
  const posterPath = `assets/posters/${slugify(movie.title)}.png`;
  const headlineTag = compact ? "h4" : "h3";
  const moodPills = movie.moods
    .slice(0, compact ? 3 : movie.moods.length)
    .map((mood) => `<span class="meta-pill">${capitalize(mood)}</span>`)
    .join("");

  return `
    <div class="${wrapperClass}">
      <div class="poster-frame">
        <img src="${posterPath}" alt="${movie.title} poster" loading="lazy" />
      </div>
      <div class="${copyClass}">
        <p class="selection-badge">${badge}</p>
        <${headlineTag}>${movie.title}</${headlineTag}>
        <p>${movie.tagline}</p>
        <div class="meta-row">
          <span class="meta-pill">${movie.year}</span>
          <span class="meta-pill">${movie.genre}</span>
          <span class="meta-pill">${movie.language}</span>
          <span class="meta-pill">Rating ${movie.rating.toFixed(1)}/10</span>
        </div>
        <p>${description}</p>
        <div class="pill-row">${moodPills}</div>
        <div class="watch-row">
          ${buildPlatformLinks(movie.title)}
        </div>
        <p class="platform-note">Links open platform search pages or a trailer search so availability stays current.</p>
      </div>
    </div>
  `;
}

function buildPlatformLinks(title) {
  const streamingLinks = state.catalog.platforms.map((platform, index) => {
    const query = encodeURIComponent(`${title} ${platform.name} watch online`);
    const href = `https://www.google.com/search?q=${query}`;
    const className = index === 0 ? "watch-link" : "watch-link secondary";
    return `<a class="${className}" href="${href}" target="_blank" rel="noreferrer">${platform.action_label}</a>`;
  });

  const trailerQuery = encodeURIComponent(`${title} official trailer`);
  streamingLinks.push(
    `<a class="watch-link secondary" href="https://www.youtube.com/results?search_query=${trailerQuery}" target="_blank" rel="noreferrer">Watch Trailer</a>`,
  );

  return streamingLinks.join("");
}

function slugify(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function capitalize(value) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

init().catch(() => {
  spotlightCard.innerHTML = "<p>Catalog could not be loaded.</p>";
  featuredResult.innerHTML = "<p>Recommendation data is unavailable right now.</p>";
});
