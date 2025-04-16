import openai
import faiss
import numpy as np

# Initialize OpenAI API
openai.api_key = 'your_openai_api_key'

def embed_text(text):
    try:
        # Generate embeddings for the given text
        response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
        embeddings = [embedding['embedding'] for embedding in response['data']]
        
        if not embeddings:
            raise ValueError(f"Empty embeddings for text: {text[:100]}...")  # Print first 100 characters for debugging
        print(f"Generated embeddings for text: {text[:100]}...")  # Debugging
        return np.array(embeddings)
    except Exception as e:
        print(f"Error embedding text: {e}")
        return np.array([])  # Return empty array if there is an issue

def store_embeddings(weekly_data):
    # Create FAISS index
    dim = 1536  # Embedding dimension (based on OpenAI's model)
    index = faiss.IndexFlatL2(dim)
    
    texts = []  # List to hold all the text summaries
    embeddings = []  # List to hold the corresponding embeddings

    # Check if weekly content is populated properly
    if not weekly_data:
        print("No weekly content available.")
        return index, texts  # Early return if there's no data
    
    for week, data in weekly_data.items():
        # Convert structured data (e.g., dict or list) to string format
        if data is None:
            week_text = f"{week}: (No content available)"
        elif isinstance(data, str):
            week_text = f"{week}: {data}"
        elif isinstance(data, dict):
            parts = []
            for key, value in data.items():
                if isinstance(value, list):
                    parts.append(f"{key.capitalize()}: {'; '.join(map(str, value))}")
                else:
                    parts.append(f"{key.capitalize()}: {value if value else 'No content available'}")  # Ensure empty content gets a placeholder
            week_text = f"{week}: " + " | ".join(parts)
        elif isinstance(data, list):
            week_text = f"{week}: " + " | ".join(map(str, data))
        else:
            week_text = f"{week}: {str(data)}"  # Convert any other type to string

        # Only proceed with weeks that have meaningful content
        if "No content available" in week_text:
            print(f"Skipping empty week: {week}")
            continue  # Skip this week if it has no meaningful content
        
        # Add the processed week text to the list
        texts.append(week_text)

        # Generate the embedding for the week text
        embedding = embed_text(week_text)
        if embedding.size > 0:
            embeddings.append(embedding)
        else:
            print(f"Skipping empty embedding for week: {week}")

    if not embeddings:
        print(f"No valid embeddings to store. Check the input text: {texts}")
        raise ValueError(f"No valid embeddings to store. Check the input text: {texts}")

    # Stack embeddings only if they are available
    index.add(np.vstack(embeddings))
    
    return index, texts
