import chromadb
import os
import uuid
from groq import Groq
from bs4 import BeautifulSoup

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "storage")
meeting_dir = os.path.join(script_dir, "meetings")

groq_key = os.getenv("GROQ_KEY", "")

print("GROQ_KEY: ", groq_key)

# Create file based ChromaDB client
settings = chromadb.get_settings()
settings.allow_reset = True
client = chromadb.PersistentClient(path=data_dir, settings=settings)

# Reset the ChromDb data
client.reset()

# Create a collection to store our meetings in
collection = client.create_collection("nddnug-meetings")

file_collection = []



for filename in os.listdir(meeting_dir):
    file_path = os.path.join(meeting_dir, filename)
    if os.path.isfile(file_path):  # Ensure it's a file
        with open(file=file_path, mode="r", encoding="utf-8") as file:
            contents = file.read() # read the file contents
            soup = BeautifulSoup(contents, 'html.parser')
            text_content = soup.get_text()
            DOC_ID = str(uuid.uuid4())  # Generate a unique ID for the document
            # Add the file contents to the ChromaDB collection
            collection.add(
                ids=[DOC_ID],
                documents=[text_content],
                metadatas=[{"filename": os.path.basename(file.name)}],
            )

query = "When was the most recent angular presentation, who presented it and what was the topic?"
results = collection.query(query_texts=[query], n_results=3)

def print_results(results):
    for index, document in enumerate(results["documents"][0]):
        print("=====================================")        
        print(f"Id: {results["ids"][0][index]}")
        print(f"Distance: {results["distances"][0][index]}")
        print(f"Meta: {results["metadatas"][0][index]}")
        print(document)
        print("=====================================")

# Uncomment to view ChromaDB results
#print(results)
#print_results(results)

def query_groq(query, results):
    messages = []

    for document in results["documents"][0]:
        messages.append({"role": "system", "content": document})

    messages.append({"role": "user", "content": query})

    groq_client = Groq(api_key=groq_key)

    chat_completion = groq_client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192")

    return chat_completion.choices[0].message.content

print(query_groq(query, results))