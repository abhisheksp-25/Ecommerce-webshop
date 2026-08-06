# geocoding.py
import json
import time
import requests
import frappe

# Nominatim policy ke hisaab se REAL contact email dena zaroori hai,
# warna requests silently block/403 ho sakte hain.
NOMINATIM_USER_AGENT = "ERPNext-Geolocation (abhishekspatil90@gmail.com)"


def update_geolocation(doc):
    if doc.custom_geolocation:
        return

    # Order fix: line1 pehle, line2 baad mein — aur city ko hata ke
    # ek fallback bhi rakha hai agar landmark-specific query fail ho.
    primary_query = ", ".join(filter(None, [
        doc.address_line1,
        doc.address_line2,
        doc.city,
        doc.state,
        doc.country,
    ]))

    coords = _geocode(primary_query)

    if not coords:
        # Fallback: sirf city/state/country se try karo, taaki kam se
        # kam approximate location toh mile (bilkul empty se better hai)
        fallback_query = ", ".join(filter(None, [doc.city, doc.state, doc.country]))
        if fallback_query and fallback_query != primary_query:
            coords = _geocode(fallback_query)

    if not coords:
        frappe.log_error(
            title="Automatic Address Geolocation",
            message=f"No geocoding result for: {primary_query}",
        )
        return

    latitude, longitude = coords

    geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Point", "coordinates": [longitude, latitude]},
        }],
    }

    doc.custom_geolocation = json.dumps(geojson)


def _geocode(address):
    """Returns (lat, lon) or None. Logs the raw response on failure for debugging."""
    if not address:
        return None

    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": address, "format": "json", "limit": 1},
            headers={"User-Agent": NOMINATIM_USER_AGENT},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        # Nominatim usage policy: max 1 request/sec
        time.sleep(1)

        if not data:
            frappe.log_error(
                title="Automatic Address Geolocation",
                message=f"Empty result for query: {address}",
            )
            return None

        return float(data[0]["lat"]), float(data[0]["lon"])

    except Exception:
        frappe.log_error(
            title="Automatic Address Geolocation",
            message=f"Query: {address}\n\n{frappe.get_traceback()}",
        )
        return None