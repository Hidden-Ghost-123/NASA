#!/usr/bin/env python3
"""
nasa.py — NASA Explorer (CLI)

Usage:
    python nasa.py apod
    python nasa.py apod --date 2024-01-15
    python nasa.py mars
    python nasa.py neo
    python nasa.py neo --hazardous           # only dangerous ones
    python nasa.py streak                    # random APOD streak challenge

Live NASA API (optional):
    NASA_API_KEY=your_key USE_DEMO_DATA=false python nasa.py apod

Free key: https://api.nasa.gov/
"""

import json, os, sys, urllib.request, urllib.parse
from datetime import date, timedelta

API_KEY       = os.getenv("NASA_API_KEY", "DEMO_KEY")
BASE_URL      = "https://api.nasa.gov"
USE_DEMO_DATA = os.getenv("USE_DEMO_DATA", "true").lower() == "true"

# ── Demo data ─────────────────────────────────────────────────────────────────
DEMO = {
    "apod": {
        "date": "2024-07-04",
        "title": "The Crab Nebula in Multiwavelength",
        "explanation": (
            "The Crab Nebula (M1) is a supernova remnant about 6,500 light-years away "
            "in Taurus. This composite combines Chandra X-ray (blue/white), Hubble (yellow), "
            "Spitzer infrared (pink), and VLT (red). At its center lies a pulsar spinning "
            "30 times per second that powers the entire nebula's glow."
        ),
        "url": "https://apod.nasa.gov/apod/image/2407/CrabMultiwavelength_HubbleXray_960.jpg",
        "copyright": "NASA, ESA, Chandra, Hubble, Spitzer",
    },
    "apod_streak": [
        {"date": "2023-11-12", "title": "Pillars of Creation (JWST)", "url": "https://apod.nasa.gov/apod/image/2311/PillarsDust_Webb_960.jpg"},
        {"date": "2024-01-08", "title": "Andromeda Galaxy in Infrared", "url": "https://apod.nasa.gov/apod/image/2401/M31_HubbleSpitzerGalex_960.jpg"},
        {"date": "2024-03-21", "title": "Jupiter's Aurora (Hubble UV)", "url": "https://apod.nasa.gov/apod/image/2403/JupiterUV_Hubble_960.jpg"},
        {"date": "2024-05-15", "title": "Perseverance Self-Portrait", "url": "https://apod.nasa.gov/apod/image/2405/PerseveranceSelf_1080.jpg"},
        {"date": "2024-06-20", "title": "Tarantula Nebula (JWST)", "url": "https://apod.nasa.gov/apod/image/2209/Tarantula2048_Webb.jpg"},
    ],
    "mars": [
        {"id":102693,"sol":1000,"earth_date":"2015-05-30","camera":{"name":"FHAZ","full_name":"Front Hazard Avoidance Camera"},"img_src":"https://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/fcam/FLB_486615455EDR_F0481570FHAZ00323M_.JPG","rover":{"name":"Curiosity","status":"active"}},
        {"id":102694,"sol":1000,"earth_date":"2015-05-30","camera":{"name":"NAVCAM","full_name":"Navigation Camera"},"img_src":"https://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/ncam/NLB_486615680EDR_F0481570NCAM00207M_.JPG","rover":{"name":"Curiosity","status":"active"}},
        {"id":102695,"sol":1000,"earth_date":"2015-05-30","camera":{"name":"MAST","full_name":"Mast Camera"},"img_src":"https://mars.jpl.nasa.gov/msl-raw-images/msss/01000/mcam/1000MR0044631400500570E01_DXXX.jpg","rover":{"name":"Curiosity","status":"active"}},
        {"id":102696,"sol":1000,"earth_date":"2015-05-30","camera":{"name":"CHEMCAM","full_name":"Chemistry and Camera Complex"},"img_src":"https://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/ccam/CR0_486630530EDR_F0481570CCAM05000M_.JPG","rover":{"name":"Curiosity","status":"active"}},
        {"id":102697,"sol":1000,"earth_date":"2015-05-30","camera":{"name":"RHAZ","full_name":"Rear Hazard Avoidance Camera"},"img_src":"https://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/rcam/RLB_486615614EDR_F0481570RHAZ00323M_.JPG","rover":{"name":"Curiosity","status":"active"}},
    ],
    "neo": {
        "element_count": 5,
        "near_earth_objects": {
            "2024-07-01": [
                {"name":"(2010 PK9)","is_potentially_hazardous_asteroid":False,"estimated_diameter":{"meters":{"estimated_diameter_min":91.7,"estimated_diameter_max":205.1}},"close_approach_data":[{"close_approach_date":"2024-07-01","relative_velocity":{"kilometers_per_hour":"48234.7"},"miss_distance":{"kilometers":"4823490.2"}}]},
                {"name":"(2015 XC352)","is_potentially_hazardous_asteroid":False,"estimated_diameter":{"meters":{"estimated_diameter_min":28.0,"estimated_diameter_max":62.6}},"close_approach_data":[{"close_approach_date":"2024-07-01","relative_velocity":{"kilometers_per_hour":"29801.3"},"miss_distance":{"kilometers":"7119342.1"}}]},
            ],
            "2024-07-02": [
                {"name":"1566 Icarus (1949 MA)","is_potentially_hazardous_asteroid":True,"estimated_diameter":{"meters":{"estimated_diameter_min":977.4,"estimated_diameter_max":2185.3}},"close_approach_data":[{"close_approach_date":"2024-07-02","relative_velocity":{"kilometers_per_hour":"104237.5"},"miss_distance":{"kilometers":"2948120.7"}}]},
                {"name":"(2019 SB6)","is_potentially_hazardous_asteroid":False,"estimated_diameter":{"meters":{"estimated_diameter_min":13.2,"estimated_diameter_max":29.5}},"close_approach_data":[{"close_approach_date":"2024-07-02","relative_velocity":{"kilometers_per_hour":"57412.9"},"miss_distance":{"kilometers":"1542978.3"}}]},
            ],
            "2024-07-03": [
                {"name":"(2019 BH)","is_potentially_hazardous_asteroid":False,"estimated_diameter":{"meters":{"estimated_diameter_min":37.3,"estimated_diameter_max":83.4}},"close_approach_data":[{"close_approach_date":"2024-07-03","relative_velocity":{"kilometers_per_hour":"72318.4"},"miss_distance":{"kilometers":"5601832.0"}}]},
            ],
        },
    },
}

# ── HTTP ──────────────────────────────────────────────────────────────────────
def _get(path, params=None):
    params = dict(params or {})
    params["api_key"] = API_KEY
    url = f"{BASE_URL}{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.loads(r.read())

# ── Helpers ───────────────────────────────────────────────────────────────────
DIV = "─" * 58

def wrap(text, width=58):
    words, lines, line = text.split(), [], ""
    for w in words:
        if len(line) + len(w) + 1 > width:
            lines.append(line); line = w
        else:
            line = (line + " " + w).strip()
    if line: lines.append(line)
    return "\n".join(lines)

def bar(pct, width=24, fill="█", empty="░"):
    n = round(pct * width)
    return fill * n + empty * (width - n)

# ── Commands ──────────────────────────────────────────────────────────────────
def cmd_apod(date_str=None):
    try:
        data = _get("/planetary/apod", {"date": date_str} if date_str else {}) if not USE_DEMO_DATA else DEMO["apod"]
    except Exception:
        data = DEMO["apod"]

    print(f"\n{DIV}")
    print(f"  {data['title']}")
    print(f"  {data['date']}" + (f"  ·  © {data['copyright']}" if data.get('copyright') else ""))
    print(DIV)
    print(wrap(data["explanation"]))
    print(f"\n  {data['url']}\n")


def cmd_mars(rover="curiosity", sol=1000, camera=None):
    try:
        params = {"sol": sol}
        if camera: params["camera"] = camera.upper()
        resp   = _get(f"/mars-photos/api/v1/rovers/{rover}/photos", params) if not USE_DEMO_DATA else {"photos": DEMO["mars"]}
        photos = resp.get("photos", [])
    except Exception:
        photos = DEMO["mars"]

    if camera:
        photos = [p for p in photos if p["camera"]["name"] == camera.upper()]

    cams = sorted(set(p["camera"]["name"] for p in photos))
    print(f"\n  Mars Rover — {rover.title()}  ·  Sol {sol}")
    print(f"  {len(photos)} photos  ·  cameras: {', '.join(cams)}\n")

    for p in photos[:5]:
        print(f"  [{p['camera']['name']:8s}]  {p['img_src']}")
    if len(photos) > 5:
        print(f"  … and {len(photos)-5} more")
    print()


def cmd_neo(hazardous_only=False):
    try:
        today = date.today()
        data  = _get("/neo/rest/v1/feed", {"start_date": str(today), "end_date": str(today + timedelta(days=6))}) if not USE_DEMO_DATA else DEMO["neo"]
    except Exception:
        data = DEMO["neo"]

    objects = sorted(
        [o for day in data["near_earth_objects"].values() for o in day],
        key=lambda o: float(o["close_approach_data"][0]["miss_distance"]["kilometers"])
    )
    if hazardous_only:
        objects = [o for o in objects if o["is_potentially_hazardous_asteroid"]]

    total    = data["element_count"]
    n_hazard = sum(1 for o in data["near_earth_objects"].values() for x in o if x["is_potentially_hazardous_asteroid"])

    # Closest miss for the proximity bar
    closest_km = float(objects[0]["close_approach_data"][0]["miss_distance"]["kilometers"]) if objects else 0

    print(f"\n  Near Earth Objects  ·  {total} total  ·  {n_hazard} hazardous")
    print(f"\n  Closest approach: {closest_km/1e6:.2f}M km")
    MAX = 10_000_000
    pct = min(closest_km / MAX, 1.0)
    print(f"  {bar(pct)}  {pct*100:.0f}% of 10M km\n")
    print(DIV)

    for o in objects:
        ca   = o["close_approach_data"][0]
        km   = float(ca["miss_distance"]["kilometers"])
        spd  = float(ca["relative_velocity"]["kilometers_per_hour"])
        d    = o["estimated_diameter"]["meters"]
        flag = "  ⚠ HAZARDOUS" if o["is_potentially_hazardous_asteroid"] else ""
        print(f"\n  {o['name']}{flag}")
        print(f"  {ca['close_approach_date']}  ·  {km/1e6:.2f}M km  ·  {spd/1000:.1f}k km/h  ·  {d['estimated_diameter_min']:.0f}–{d['estimated_diameter_max']:.0f} m")

    print()


def cmd_streak():
    """Show a random sequence of APOD picks — a discovery streak."""
    import random
    entries = DEMO["apod_streak"]
    random.shuffle(entries)
    print(f"\n  🌌  APOD Discovery Streak  —  {len(entries)} picks\n")
    for i, e in enumerate(entries, 1):
        print(f"  {i}.  [{e['date']}]  {e['title']}")
        print(f"       {e['url']}")
    print()


# ── Entry ─────────────────────────────────────────────────────────────────────
def main():
    mode = "demo" if USE_DEMO_DATA else f"live (key: {API_KEY[:4]}…)"
    print(f"\n🚀  NASA Explorer  [{mode}]")

    args = sys.argv[1:]
    cmd  = args[0] if args else None

    if cmd == "apod":
        date_arg = next((a for a in args[1:] if a.startswith("--date=") or not a.startswith("-")), None)
        if date_arg and date_arg.startswith("--date="):
            date_arg = date_arg.split("=", 1)[1]
        cmd_apod(date_arg)

    elif cmd == "mars":
        rover  = next((a.split("=",1)[1] for a in args[1:] if a.startswith("--rover=")),  "curiosity")
        sol    = int(next((a.split("=",1)[1] for a in args[1:] if a.startswith("--sol=")),    1000))
        camera = next((a.split("=",1)[1] for a in args[1:] if a.startswith("--camera=")), None)
        cmd_mars(rover, sol, camera)

    elif cmd == "neo":
        hazardous = "--hazardous" in args
        cmd_neo(hazardous)

    elif cmd == "streak":
        cmd_streak()

    else:
        print("""
  Commands:
    apod                     Astronomy Picture of the Day
    apod --date=YYYY-MM-DD   Pick a specific date
    mars                     Mars Rover photos (Curiosity, Sol 1000)
    mars --camera=NAVCAM     Filter by camera
    neo                      Near-Earth asteroid feed
    neo --hazardous          Only show potentially hazardous ones
    streak                   Random APOD discovery picks

  Options:
    NASA_API_KEY=your_key    Use your own API key (api.nasa.gov)
    USE_DEMO_DATA=false       Fetch live data instead of demo
""")

if __name__ == "__main__":
    main()
