from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def compare_sentences_google(sentence1: str, sentence2: str) -> float:
    """
    Compares two sentences using Google's text embedding model and cosine similarity.

    Args:
        sentence1: The first sentence.
        sentence2: The second sentence.

    Returns:
        The cosine similarity between the two sentences using the cosine_similarity function.
        A score of 1.0 indicates identical sentences (after embedding), while 0.0 means no similarity.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Embed the sentences
    embedding1 = embeddings.embed_query(sentence1)
    embedding2 = embeddings.embed_query(sentence2)

    # Calculate cosine similarity
    similarity = cosine_similarity(np.array(embedding1).reshape(1, -1), np.array(embedding2).reshape(1, -1))
    similarity = cosine_similarity(np.array(embedding1).reshape(1, -1), np.array(embedding2).reshape(1, -1))
    similarity_score = similarity[0][0]
    
    return similarity_score


