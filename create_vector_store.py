from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

from bs4 import BeautifulSoup
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_voyageai import VoyageAIEmbeddings

from configs import Config


def extract_text_from_html(html_content: bytes) -> str:
    soup = BeautifulSoup(html_content, 'html.parser', from_encoding="iso-8859-8")
    docs_body = soup.find('div', id='docs-body')
    return docs_body.text if docs_body else ''


def get_latest_sqlalchemy_docs() -> list[Document]:
    folders_to_extract_data_from = tuple("faq/")
    print("Downloading SQLAlchemy documents...")
    resp = urlopen("https://docs.sqlalchemy.org/20/sqlalchemy_20.zip")
    print("Extracting SQLAlchemy documents...")
    archive = ZipFile(BytesIO(resp.read()))

    docs_text = []
    for file_name in archive.namelist():
        if file_name.startswith(folders_to_extract_data_from):
            if docs_html := archive.read(file_name):  # BSHTMLLoader expects a file path, so we use Document
                docs_text.append(Document(page_content=extract_text_from_html(docs_html),
                                          metadata={"source": file_name}))

    return docs_text


def split_text_into_chunks(documents: list[Document]) -> list[Document]:
    print("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50, length_function=len,
                                                   add_start_index=True)
    doc_chunks = text_splitter.split_documents(documents)
    return doc_chunks


def save_into_faiss(doc_chunks: list[Document], embeddings: VoyageAIEmbeddings):
    print("Ingesting embeddings...")
    db = FAISS.from_documents(doc_chunks, embeddings)
    db.save_local(Config.DB_NAME)
    print(f"Saved {db.index.ntotal} chunks into FAISS.")


if __name__ == "__main__":
    documentation = get_latest_sqlalchemy_docs()
    chunks = split_text_into_chunks(documentation)
    save_into_faiss(chunks, Config.VOYAGE_AI_EMBEDDINGS)
