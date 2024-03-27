"""
I opted for longer line lengths, deviating from PEP8's recommendation of 79 characters, primarily due to modern screen
resolutions. With screens capable of displaying more content, adhering strictly to the 79-character limit can lead to
less visually appealing and harder-to-read code.

Therefore, I've opted for the line length to 120 characters (default settings in PyCharm).
"""
from fastapi import FastAPI, Response, Query, Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from uvicorn.config import LOGGING_CONFIG

from configs import Config
from create_vector_store import get_latest_sqlalchemy_docs, split_text_into_chunks, save_into_faiss
from process_query import generate_response

app = FastAPI(title="RAG for SQLAlchemy")
api_key_header = APIKeyHeader(name='Authorization')


async def verify_token(authorization: str = Security(api_key_header)):
    # This is for illustrative purposes only, please don't use in production :D
    if authorization != Config.HARDCODED_EXAMPLE_TOKEN:
        raise HTTPException(status_code=401, detail="Could not validate credentials.")


@app.get("/create_vector", dependencies=[Depends(verify_token)])
async def create_faiss_database():
    """ Create vectors from the latest SQLAlchemy documentation and saves them into a FAISS index.
    It may take a minute to retrieve the documentation from the web and embed it. """
    documentation = get_latest_sqlalchemy_docs()
    chunks = split_text_into_chunks(documentation)
    save_into_faiss(chunks, Config.VOYAGE_AI_EMBEDDINGS)
    return Response(content="Database created successfully.", status_code=status.HTTP_201_CREATED)


@app.get("/ask", dependencies=[Depends(verify_token)])
async def ask_ai(query: str = Query(description="The question you want to ask the AI.",
                                    examples=["What criteria are used to deduplicate a list of ORM-mapped objects?"])):
    """ This endpoint accepts a query and returns a response from the AI. It requires a valid token to be passed in
    the headers. """
    return generate_response(query)


if __name__ == "__main__":
    import uvicorn

    formatter = "%(asctime)s | %(levelname)s - %(process)s | %(name)s"
    LOGGING_CONFIG["formatters"]["default"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = f"{formatter} | %(message)s "
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = f"{formatter} | %(request_line)s | " \
                                                    f"%(status_code)s | %(client_addr)s"

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug")
