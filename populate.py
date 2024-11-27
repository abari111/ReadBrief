import os
from dotenv import load_dotenv

import openai
from pinecone import Pinecone

load_dotenv()
# OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index("abaribot")

def chunk_docs(file_path, chunk_strat=None, num_char=100):
    with open(file_path) as fp:
        content = fp.read()
    chunks = []
    num_chunks = len(content)/num_char
    for i in range(num_chunks):
        chunk = content[i*num_char:num_char + i*num_char]

def populate_chunk(chunk, doc_id):
    try:
        # Read the content of the file

        # Generate embeddings for the content
        embedding_response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=chunk
        )
        content_embedding = embedding_response.data[0].embedding

        # Store the embeddings in Pinecone
        index.upsert([{
            "id": doc_id,
            "values": content_embedding,
            "metadata": {"content": chunk}
        }])

        print(f"Successfully populated vector database with document ID: {doc_id}")
    except Exception as e:
        print(f"Error populating vector database: {str(e)}")
        
def populate(file_path, doc_id):
    """
    Populate the vector database with embeddings from a text file.

    Args:
        file_path (str): Path to the text file.
        doc_id (str): Unique identifier for the document in the vector database.
    """
    try:
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Generate embeddings for the content
        embedding_response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=content
        )
        content_embedding = embedding_response.data[0].embedding

        # Store the embeddings in Pinecone
        index.upsert([{
            "id": doc_id,
            "values": content_embedding,
            "metadata": {"content": content}
        }])

        print(f"Successfully populated vector database with document ID: {doc_id}")
    except Exception as e:
        print(f"Error populating vector database: {str(e)}")

# Example Usage
if __name__ == "__main__":
    populate("abari.txt", doc_id="doc-1")
