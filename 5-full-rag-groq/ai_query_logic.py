import chromadb
from nomic import embed
import numpy as np
from groq import Groq
import os
from termcolor import colored

client = chromadb.HttpClient()
coll = client.get_or_create_collection("custom_pdfs_1")


def get_matching_chunks(question):
    output = embed.text(
        texts=[question],
        model='nomic-embed-text-v1.5',
    )

    embeddings = np.array(output['embeddings'])

    formatted_numbers = [f"{num:.8f}" for num in embeddings[0]]
    comma_delimited_string = ", ".join(formatted_numbers)
    print(comma_delimited_string)

    results = coll.query(
        n_results=2,
        query_embeddings=embeddings
        # where={"metadata_field": "is_equal_to_this"}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
    )

    return results


def make_query(question):

    matching_chunks = get_matching_chunks(question)

    chat_background = []

    for k in matching_chunks:
        if k == "documents":
            for document_text in matching_chunks[k][0]:

                # Appends the doc text from matching results
                chat_background.append({
                    "role": "system",
                    "content": document_text
                })


    chat_background.append({"role": "user", "content": "You: " + question})

    ## Groq time

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_background,
        # max_tokens=100,
        temperature=1.2
    )

    print("")
    print(colored("The question: " + question, "green"))
    print("")

    print(chat_completion.choices[0].message.content)
    print("")

    return chat_completion
