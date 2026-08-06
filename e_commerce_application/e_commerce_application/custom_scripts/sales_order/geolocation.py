#geolocation.py
import json
def get_coordinates(address_doc):
    """
    Extract latitude and longitude from Address Geolocation field.

    Returns:
        (latitude, longitude) or (None, None)
    """

    if not address_doc.custom_geolocation:
        return None, None

    try:
        geojson = address_doc.custom_geolocation

        # If stored as string, convert to dict
        if isinstance(geojson, str):
            geojson = json.loads(geojson)

        features = geojson.get("features", [])

        if not features:
            return None, None

        geometry = features[0].get("geometry", {})

        if geometry.get("type") != "Point":
            return None, None

        coordinates = geometry.get("coordinates", [])

        if len(coordinates) != 2:
            return None, None

        longitude = coordinates[0]
        latitude = coordinates[1]

        return latitude, longitude

    except Exception:
        return None, None