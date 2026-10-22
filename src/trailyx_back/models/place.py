from typing import Optional
from beanie import Document

class Place(Document):
	country: str
	city: str
	place_name: Optional[str] = None
	lat: Optional[float] = None
	lng: Optional[float] = None

	class Settings:
		name = "places"
