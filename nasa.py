#!/usr/bin/env python3
"""
nasa.py — NASA Explorer
Explore APOD, Mars Rover photos, and Near-Earth Objects.

Usage:
    python nasa.py apod
    python nasa.py mars
    python nasa.py neo

Uses bundled demo data by default. To use the real NASA API:
    NASA_API_KEY=mU9zbe5WjHtdWsHJzzlChacuCRm8WqHQyDUMSbr6=false python nasa.py apod

Free API key: https://api.nasa.gov/
"""

import json
import os
import sys

API_KEY       = os.getenv("NASA_API_KEY", "DEMO_KEY")
BASE_URL      = "https://api.nasa.gov"
USE_DEMO_DATA = os.getenv("USE_DEMO_DATA", "true").lower() == "true"

DEMO = {
    "apod": {
        "date": "2024-07-04",
        "title": "The Crab Nebula in Multiwavelength",
        "explanation": (
            "The Crab Nebula (M1) is a supernova remnant about 6,500 light-years away in "
            "Taurus. This composite combines data from Chandra X-ray (blue/white), Hubble "
            "(yellow), Spitzer infrared (pink), and VLT (red), each wavelength revealing a "
            "different layer of the expanding debris cloud. At the center lies a pulsar — a "
            "rapidly rotating neutron star spinning 30 times per second — which powers the "
            "entire nebula's glow. The Crab spans roughly 11 light-years and is one of the "
            "most-studied objects in the night sky."
        ),
        "url": "https://apod.nasa.gov/apod/image/2407/CrabMultiwavelength_HubbleXray_960.jpg",
        "hdurl": "https://apod.nasa.gov/apod/image/2407/CrabMultiwavelength_HubbleXray_3600.jpg",
        "media_type": "image",
        "copyright": "NASA, ESA, Chandra, Hubble, VLT, Spitzer",
    },

    "mars": [
        {
            "id": 102693, "sol": 1000, "earth_date": "2015-05-30",
            "camera": {"name": "FHAZ", "full_name": "Front Hazard Avoidance Camera"},
            "img_src": "https://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/fcam/FLB_486615455EDR_F0481570FHAZ00323M_.JPG",
            "rover": {"name": "Curiosity", "status": "active", "landing_date": "2012-08-06"},
        },
        {
            "id": 102694, "sol": 1000, "earth_date": "2015-05-30",
            "camera": {"name": "NAVCAM", "full_name": "Navigation Camera"},
            "img_src": "https://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/ncam/NLB_486615680EDR_F0481570NCAM00207M_.JPG",
            "rover": {"name": "Curiosity", "status": "active", "landing_date": "2012-08-06"},
        },
        {
            "id": 102695, "sol": 1000, "earth_date": "2015-05-30",
            "camera": {"name": "MAST", "full_name": "Mast Camera"},
            "img_src": "https://mars.jpl.nasa.gov/msl-raw-images/msss/01000/mcam/1000MR0044631400500570E01_DXXX.jpg",
            "rover": {"name": "Curiosity", "status": "active", "landing_date": "2012-08-06"},
        },
        {
            "id": 102696, "sol": 1000, "earth_date": "2015-05-30",
            "camera": {"name": "CHEMCAM", "full_name": "Chemistry and Camera Complex"},
            "img_src": "https://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/ccam/CR0_486630530EDR_F0481570CCAM05000M_.JPG",
            "rover": {"name": "Curiosity", "status": "active", "landing_date": "2012-08-06"},
        },
        {
            "id": 102697, "sol": 1000, "earth_date": "2015-05-30",
            "camera": {"name": "RHAZ", "full_name": "Rear Hazard Avoidance Camera"},
            "img_src": "https://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/rcam/RLB_486615614EDR_F0481570RHAZ00323M_.JPG",
            "rover": {"name": "Curiosity", "status": "active", "landing_date": "2012-08-06"},
        },
    ],

    "neo": {
        "element_count": 5,
        "near_earth_objects": {
            "2024-07-01": [
                {
                    "name": "(2010 PK9)",
                    "is_potentially_hazardous_asteroid": False,
                    "estimated_diameter": {"meters": {"estimated_diameter_min": 91.7, "estimated_diameter_max": 205.1}},
                    "close_approach_data": [{"close_approach_date": "2024-07-01",
                        "relative_velocity": {"kilometers_per_hour": "48234.7"},
                        "miss_distance": {"kilometers": "4823490.2"}}],
                },
                {
                    "name": "(2015 XC352)",
                    "is_potentially_hazardous_asteroid": False,
                    "estimated_diameter": {"meters": {"estimated_diameter_min": 28.0, "estimated_diameter_max": 62.6}},
                    "close_approach_data": [{"close_approach_date": "2024-07-01",
                        "relative_velocity": {"kilometers_per_hour": "29801.3"},
                        "miss_distance": {"kilometers": "7119342.1"}}],
                },
            ],
            "2024-07-02": [
                {
                    "name": "1566 Icarus (1949 MA)",
                    "is_potentially_hazardous_asteroid": True,
                    "estimated_diameter": {"meters": {"estimated_diameter_min": 977.4, "estimated_diameter_max": 2185.3}},
                    "close_approach_data": [{"close_approach_date": "2024-07-02",
                        "relative_velocity": {"kilometers_per_hour": "104237.5"},
                        "miss_distance": {"kilometers": "2948120.7"}}],
                },
                {
                    "name": "(2019 SB6)",
                    "is_potentially_hazardous_asteroid": False,
                    "estimated_diameter": {"meters": {"estimated_diameter_min": 13.2, "estimated_diameter_max": 29.5}},
                    "close_approach_data": [{"close_approach_date": "2024-07-02",
                        "relative_velocity": {"kilometers_per_hour": "57412.9"},
                        "miss_distance": {"kilometers": "1542978.3"}}],
                },
            ],
            "2024-07-03": [
                {
                    "name": "(2019 BH)",
                    "is_potentially_hazardous_asteroid": False,
                    "estimated_diameter": {"meters": {"estimated_diameter_min": 37.3, "estimated_diameter_max": 83.4}},
                    "close_approach_data": [{"close_approach_date": "2024-07-03",
                        "relative_velocity": {"kilometers_per_hour": "72318.4"},
                        "miss_distance": {"kilometers": "5601832.0"}}],
                },
            ],
        },
    },
}

def _get(path: str, params: dict = None) -> any:
    """Make a GET request to the NASA API and return parsed JSON."""
    import urllib.request, urllib.parse
    params = params or {}
    params["api_key"] = API_KEY
    url = f"{BASE_URL}{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.loads(resp.read())

def cmd_apod():
    if USE_DEMO_DATA:
        data = DEMO["apod"]
    else:
        data = _get("/planetary/apod")

    print("=" * 60)
    print(f"  {data['title']}")
    print(f"  Date : {data['date']}")
    if data.get("copyright"):
        print(f"  Credit: {data['copyright']}")
    print("=" * 60)
    words, line = data.get("explanation", "").split(), ""
    for word in words:
        if len(line) + len(word) + 1 > 60:
            print(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        print(line)
    print()
    print(f"  URL  : {data.get('url', 'N/A')}")
    if data.get("hdurl"):
        print(f"  HD   : {data['hdurl']}")
    print()


def cmd_mars(rover="curiosity", sol=1000):
    if USE_DEMO_DATA:
        photos = DEMO["mars"]
    else:
        resp = _get(f"/mars-photos/api/v1/rovers/{rover}/photos", {"sol": sol})
        photos = resp.get("photos", [])

    print(f"  Mars Rover Photos — {rover.title()}, Sol {sol}")
    print(f"  {len(photos)} photo(s) found\n")
    for p in photos[:5]:
        print(f"  ID     : {p['id']}")
        print(f"  Rover  : {p['rover']['name']}  ({p['rover']['status']})")
        print(f"  Camera : {p['camera']['full_name']}")
        print(f"  Date   : {p['earth_date']}  (Sol {p['sol']})")
        print(f"  URL    : {p['img_src']}")
        print()


def cmd_neo():
    if USE_DEMO_DATA:
        data = DEMO["neo"]
    else:
        from datetime import date, timedelta
        start = date.today()
        end = start + timedelta(days=6)
        data = _get("/neo/rest/v1/feed", {"start_date": str(start), "end_date": str(end)})

    total = data["element_count"]
    neo_dates = data["near_earth_objects"]

    hazardous = [
        obj for objects in neo_dates.values() for obj in objects
        if obj["is_potentially_hazardous_asteroid"]
    ]

    print(f"  Near Earth Objects — {total} total, {len(hazardous)} potentially hazardous\n")
    for day, objects in sorted(neo_dates.items()):
        for obj in objects:
            ca = obj["close_approach_data"][0]
            diam = obj["estimated_diameter"]["meters"]
            flag = "    HAZARD" if obj["is_potentially_hazardous_asteroid"] else ""
            print(f"  [{ca['close_approach_date']}] {obj['name']}{flag}")
            print(f"    Miss distance : {float(ca['miss_distance']['kilometers']):>14,.0f} km")
            print(f"    Speed         : {float(ca['relative_velocity']['kilometers_per_hour']):>14,.0f} km/h")
            print(f"    Est. diameter : {diam['estimated_diameter_min']:.0f} – {diam['estimated_diameter_max']:.0f} m")
            print()

COMMANDS = {"apod": cmd_apod, "mars": cmd_mars, "neo": cmd_neo}

def main():
    mode = "demo" if USE_DEMO_DATA else f"live (key: {API_KEY[:4]}...)"
    print(f"\n  NASA Explorer  [{mode}]\n")

    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd not in COMMANDS:
        print("Usage:  python nasa.py [apod | mars | neo]\n")
        print("  apod  — Astronomy Picture of the Day")
        print("  mars  — Mars Rover photos (Curiosity, Sol 1000)")
        print("  neo   — Near Earth Objects / asteroid feed")
        print()
        print("Options (environment variables):")
        print("  USE_DEMO_DATA=false   — use real NASA API instead of demo data")
        print("  NASA_API_KEY=your_key — your API key from https://api.nasa.gov/")
        sys.exit(0 if cmd is None else 1)

    COMMANDS[cmd]()

if __name__ == "__main__":
    main()
