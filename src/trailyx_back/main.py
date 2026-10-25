from fastapi import FastAPI
from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient
from beanie import init_beanie
from trailyx_back.core.config import settings
from trailyx_back.models.place import Place
from trailyx_back.models.post import Post
from fastapi import UploadFile, Form
from beanie import PydanticObjectId
from trailyx_back.utils import extract_gps, reverse_geocode
import os
os.environ["CLOUDINARY_URL"] = settings.cloudinary_url

import cloudinary
import cloudinary.uploader

@asynccontextmanager
async def lifespan(app: FastAPI):
	print("Starting up...")
	client = AsyncMongoClient(settings.mongodb_url)
	await init_beanie(database=client.get_default_database(), document_models=[Place, Post])
	yield
	print("Shutting down...")

app = FastAPI(lifespan=lifespan)

# place
@app.get('/place')
async def get_places() -> list[Place]:
	places = await Place.find_all().to_list()
	return places
	
@app.post('/place')
async def create_place(place: Place) -> Place:
	await place.insert()
	return place

# post
@app.get('/post')
async def get_posts() -> list[Post]:
	posts = await Post.find_all().to_list()
	return posts

@app.post('/post')
async def create_post(file: UploadFile, place_id: PydanticObjectId = Form(...)) -> Post:
	contents = await file.read()
	result = cloudinary.uploader.upload(contents)

	post = Post(
		user_id="test",
		place_id=place_id,
		image_src=result["secure_url"]
	)

	await post.insert()
	return post
