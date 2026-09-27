import os
from pathlib import Path

import feedparser

from rss_agent.file_parser import parse_file

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

hugg_embedding_func = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

feed_ids: list[str] = []


def create_vector_store_db(documents: list[Document]) -> Chroma:
    chroma_db = Chroma.from_documents(
        documents=documents,
        embedding=hugg_embedding_func,
        persist_directory="./chroma_db",
        collection_name="rss-collection"
    )
    return chroma_db


def add_document(documents: list[Document]) -> Chroma:
    chroma_db = Chroma(
        collection_name="rss-collection",
        embedding_function=hugg_embedding_func,
        persist_directory="./chroma_db"
    )
    chroma_db.add_documents(documents)
    return chroma_db


def add_rss_document(rss_feed_url: str):
    feed_parser = feedparser.parse(rss_feed_url)
    print(feed_parser)
    documents: list[Document] = []
    for entry in feed_parser.entries:
        if not is_new_feed(entry.id):
            continue
        title = entry.title
        description = entry.summary
        link = entry.link
        print(f"[Title] {title}")
        print(f"[Description] {description}")
        print(f"[Link] {link}")
        enclosure = None
        for per_link in entry.links:
            if per_link["rel"] == "enclosure":
                enclosure_href = per_link["href"]
                length = per_link["length"]
                type = per_link["type"]
                href_content = parse_file(enclosure_href)
                print(f"[Enclosure] {Path(enclosure_href).as_uri()}, {length}, {type}")
                print(href_content)
                documents.append(Document(page_content=href_content, metadata={
                    "source": enclosure_href,
                    "length": length,
                    "description": description
                }))
        contents = entry.content
        for content in contents:
            print(f"[Content] {content["value"]}")
        print()

    if len(documents) != 0:
        if os.path.exists("../chroma_db"):
            return add_document(documents)
        else:
            return create_vector_store_db(documents)
    return None


def search_vector_db(query: str) -> list[Document]:
    chroma_db = Chroma(
        collection_name="rss-collection",
        embedding_function=hugg_embedding_func,
        persist_directory="./chroma_db"
    )
    return chroma_db.similarity_search(query=query, k=2)


def is_new_feed(feed_id: str) -> bool:
    if feed_id in feed_ids:
        return False
    else:
        feed_ids.append(feed_id)
        return True
