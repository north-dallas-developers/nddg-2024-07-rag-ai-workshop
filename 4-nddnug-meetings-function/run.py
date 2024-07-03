import chromadb
import os
import uuid
import re
import json
from groq import Groq
from bs4 import BeautifulSoup
from datetime import datetime

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
            file_name = os.path.basename(file.name)
            match = re.search(r"(\d{4})-(\d{2})-\d{2}", file_name)
            month = match.group(2)
            year = match.group(1)
            DOC_ID = str(uuid.uuid4())  # Generate a unique ID for the document
            # Add the file contents to the ChromaDB collection
            collection.add(
                ids=[DOC_ID],
                documents=[text_content],
                metadatas=[{"filename": file_name, "month": month, "year": year, "date": match.group(0)}],
            )

query = "Give me the details of the third meeting."
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

def get_meeting_by_index(index: int):
    
    print("Fetching Index: ", index)

    # Retrieve all documents
    results = collection.get()  # Adjust n_results as needed to fetch all documents
    documents = results['documents']
    metadatas = results['metadatas']
    
    # Combine documents with their metadata
    combined = list(zip(documents, metadatas))
    
    # Sort documents by date in metadata
    def extract_date(metadata):
        return datetime.strptime(metadata['date'], '%Y-%m-%d')
    
    sorted_combined = sorted(combined, key=lambda x: extract_date(x[1]))
    
    if(index == -1):
        return sorted_combined[len(sorted_combined)-1][0]
    else:
        return sorted_combined[index][0]

def query_groq(query, results):
    messages = [{
        "role": "system",
        "content": '''You are a function calling LLM that uses the data extracted from the 
                    get_meeting_by_index function to answer questions around user group meetings.'''
    }]

    #for document in results["documents"][0]:
    #    messages.append({"role": "system", "content": document})

    messages.append({"role": "user", "content": query})

    groq_client = Groq(api_key=groq_key)
    MODEL = "llama3-70b-8192"

    chat_completion = groq_client.chat.completions.create(
        messages=messages,
        model=MODEL,
        tools = [
        {
            "type": "function",
            "function": {
                "name": "get_meeting_by_index",
                "description": "Retrieve the content of the nth meeting. It should take precedence over previous system messages.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "index": {
                            "type": "integer",
                            "description": "The index of the meeting to retrieve. Use -1 to get the most recent meeting. 1 for the first meeting and so on.",
                        }
                    },
                    "required": ["index"],
                },
            },
        }
    ])

    response_message = chat_completion.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_meeting_by_index": get_meeting_by_index,
        }  # only one function in this example, but you can have multiple
        #messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                index=function_args.get("index")
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = groq_client.chat.completions.create(
            model=MODEL,
            messages=messages
        )  # get a new response from the model where it can see the function response
        return second_response.choices[0].message.content
    else:
        return chat_completion.choices[0].message.content



print(query_groq(query, results))
#print(get_meeting_by_index(0))