import json, os, datetime, urllib.request

NOAA_URL = "https://api.weather.gov/alerts/active"
OUTPUT_PATH = "data/alerts.json"

def fetch():
    req = urllib.request.Request(NOAA_URL, headers={"User-Agent": "github.com/rahulwork247/noaa-weather-alerts"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.load(resp)
    simplified = []
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        simplified.append({
            "id": props.get("id"),
            "event": props.get("event"),
            "severity": props.get("severity"),
            "certainty": props.get("certainty"),
            "urgency": props.get("urgency"),
            "areaDesc": props.get("areaDesc"),
            "effective": props.get("effective"),
            "expires": props.get("expires"),
            "description": props.get("description"),
            "instruction": props.get("instruction"),
        })
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump({"generated": datetime.datetime.utcnow().isoformat() + "Z", "alerts": simplified}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch()
