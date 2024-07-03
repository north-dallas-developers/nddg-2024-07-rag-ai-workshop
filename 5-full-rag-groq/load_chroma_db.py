from pypdf import PdfReader
import os
import chromadb
from chromadb.config import Settings
from nomic import embed
import numpy as np


# Connect to Chroma
client = chromadb.HttpClient()
coll = client.get_or_create_collection("custom_pdfs_1")


def load_documents(collection):

    # Process documents

    directory = "documents"
    for filename in os.listdir(directory):
        print('filename: ' + filename)
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            chunks = chunk_text(text, 1000, 400)

            embeddings = np.array(generate_embeddings(chunks)['embeddings'])

            add_chunks_to_chromadb(chunks, embeddings, collection, filename)

def add_chunks_to_chromadb(chunks, embeddings, collection, filename):

    ids = []
    metadatas = []
    idx = 0
    for chunk in chunks:
        ids.append(filename + str(idx))
        metadatas.append({"source": filename})
        idx = idx + 1
    # print(ids)

    collection.add(
        documents=chunks, # we embed for you, or bring your own
        metadatas=metadatas, # filter on arbitrary metadata!
        ids=ids, # must be unique for each doc 
        embeddings = embeddings,
    )

def chunk_text(text, chunk_size, step_size):
    # Generate chunks using a sliding window approach
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), step_size)]
    return chunks

def generate_embeddings(chunks):
    output = embed.text(
        texts=chunks,
        model='nomic-embed-text-v1.5',
    )
    return output


load_documents(coll)