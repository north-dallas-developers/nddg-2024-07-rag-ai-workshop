import os
from llama_index.llms import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader 

os.environ["OPENAI_API_KEY"] = ""

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "files")

# how to use chromadb instead of this in-memory store
documents = SimpleDirectoryReader(data_dir).load_data()
index = VectorStoreIndex.from_documents(documents) #how to chage this
index.storage_context.persist()

query_engine = index.as_query_engine()


while True:
    input_string = input()
    response = query_engine.query(input_string)

    print(response)

    print("")
    print("Ask another question !")
