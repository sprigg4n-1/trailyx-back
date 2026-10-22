from typing import Optional
from beanie import Document
from beanie import PydanticObjectId
from datetime import datetime
from pydantic import Field

class Post(Document):
	user_id: str
	place_id: PydanticObjectId
	image_src: str
	caption: Optional[str] = None
	taken_at: Optional[datetime] = None
	created_at: datetime = Field(default_factory=datetime.utcnow)

	class Settings:
		name = "posts"