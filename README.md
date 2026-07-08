# NASA
Pulls live data from NASA's completely free public APIs and puts it in your terminal. Track asteroid close approaches with a custom danger scoring algorithm, watch the ISS move in real time, browse Mars rover photos, get today's Astronomy Picture of the Day and monitor solar weather events.

---
# DEVLOG 1 
Been reading api.nasa.gov docs for the past hour. Way more data than I expected. APOD, asteroids, Mars photos, space weather, satellite imagery. Some endpoints don't even need a key.

Wrote the simplest possible test before building anything:

<img width="408" height="430" alt="image" src="https://github.com/user-attachments/assets/d5d88564-e949-4525-b5ac-dc8f6e705440" />


Been reading api.nasa.gov docs for the past hour. Way more data than I expected. APOD, asteroids, Mars photos, space weather, satellite imagery — all free. Some endpoints don't even need a key.

Wrote the simplest possible test before building anything. set up the folder structure. coded the first parts of the config.py . 

---

#DEVLOG 2 - 3 

### 2 Enhanced the NASA API client with built in rate limiting and robust error handling to improve reliability and prevent API abuse. Requests are automatically throttled, include custom application headers, and gracefully handle timeouts, connection failures, invalid API keys and rate limit errors.

Added a custom NASAAPIError exception system, providing clear and user-friendly error messages that make debugging and troubleshooting API issues much easier.
Been reading api.nasa.gov docs for the past hour. Way more data than I expected. APOD, asteroids, Mars photos, space weather, satellite imagery — all free. Some endpoints don't even need a key.

Wrote the simplest possible test before building anything. set up the folder structure. coded the first parts of the config.py . 

### 3 i Built the first version of the NASA client, enabling access to "astronomy Picture of the day" (APOD), Near Earth object (NEO) feeds, and Mars Rover mission data through reusable API request methods. ... looking to add error handling next as it is not in place at the moment 

<img width="408" height="430" alt="Screenshot 2026-06-12 123457" src="https://github.com/user-attachments/assets/aacc52d0-39b4-4ee5-b398-98f2f30c433e" />


<img width="444" height="440" alt="Screenshot 2026-06-12 164829" src="https://github.com/user-attachments/assets/2d466a69-a851-47a6-ab87-7aeded90240e" />


# NASA Explorer

Browse NASA's public data — Astronomy Picture of the Day, Mars Rover photos, and Near-Earth Objects.

**Two versions:**
- `index.html` — runs in any browser, playable on itch.io
- `nasa.py` — command-line version, no extra setup

---

## Play it (itch.io)

Open `index.html` directly in a browser, or upload it to itch.io:

1. Zip just `index.html`
2. Upload the zip to your itch.io project
3. Set *Kind of project* → **HTML**, check **This file will be played in the browser**

No server needed. The app calls the NASA API live and falls back to bundled demo data if the request fails.

---

## CLI version

```bash
pip install requests       # only needed for live API mode
python nasa.py apod        # Astronomy Picture of the Day
python nasa.py apod --date=2024-06-01
python nasa.py mars        # Mars Rover photos
python nasa.py mars --camera=NAVCAM
python nasa.py neo         # Near-Earth asteroid feed
python nasa.py neo --hazardous
python nasa.py streak      # random APOD discovery picks
```

---

## Live NASA data (optional)

The app works out of the box with bundled demo data.  
To fetch real live data, get a free key at [api.nasa.gov](https://api.nasa.gov/) (no credit card):

```bash
# CLI
NASA_API_KEY=your_key USE_DEMO_DATA=false python nasa.py apod

# HTML — open index.html, find this line near the top of the <script>:
#   const API_KEY = 'DEMO_KEY';
# Replace DEMO_KEY with your key and save.
```

---

## Files

| File | What it is |
|------|-----------|
| `index.html` | Self-contained browser app (itch.io ready) |
| `nasa.py` | CLI — APOD, Mars, NEO, streak mode |
| `requirements.txt` | Python deps (only `requests`) |

