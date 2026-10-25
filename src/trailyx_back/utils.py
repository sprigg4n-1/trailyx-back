from exif import Image as ExifImage

import httpx

NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"
NOMINATIM_HEADERS = {"User-Agent": "Trailyx (koviniaroman.mg@gmail.com)"}


async def reverse_geocode(lat: float, lng: float) -> dict | None:
    params = {"lat": lat, "lon": lng, "format": "jsonv2"}

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(NOMINATIM_URL, params=params, headers=NOMINATIM_HEADERS)
            response.raise_for_status()
    except httpx.HTTPError:
        return None

    address = response.json().get("address", {})

    return {
        "country": address.get("country"),
        "city": address.get("city") or address.get("town") or address.get("village"),
        "place_name": address.get("tourism") or address.get("attraction") or address.get("amenity"),
    }


def _dms_to_decimal(dms: tuple[float, float, float], ref: str) -> float:
    degrees, minutes, seconds = dms
    decimal = degrees + minutes / 60 + seconds / 3600
    return -decimal if ref in ("S", "W") else decimal


def extract_gps(contents: bytes) -> tuple[float, float] | None:
    try:
        img = ExifImage(contents)
        if not img.has_exif:
            return None
        lat = _dms_to_decimal(img.gps_latitude, img.gps_latitude_ref)
        lng = _dms_to_decimal(img.gps_longitude, img.gps_longitude_ref)
    except Exception:
        # Not a JPEG, no GPS tags, or partial GPS data
        return None
    return lat, lng
