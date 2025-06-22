from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def VectorSimilaritySearch(Query,Vectors,Top_n=3):

    similarity_scores = cosine_similarity(Query, Vectors)
    most_similar_indices = np.argsort(similarity_scores)[0][-Top_n:]
    return most_similar_indices

