from os import getenv

from dotenv import load_dotenv
from langchain_voyageai import VoyageAIEmbeddings


class Config:
    load_dotenv()
    DB_NAME = getenv("DB_NAME")
    HARDCODED_EXAMPLE_TOKEN = getenv("REST_API_TOKEN")

    # I chose to use the second model from "overall MTEB English leaderboard"
    VOYAGE_AI_EMBEDDINGS = VoyageAIEmbeddings(model="voyage-lite-02-instruct", batch_size=7)
