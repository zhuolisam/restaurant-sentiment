import os
from sklearn.feature_extraction.text import TfidfVectorizer

cache_folder = os.path.join(os.getcwd(), "models")
from sentence_transformers import SentenceTransformer

def embedding(documents, embedding='sbert'):
    if embedding == 'sbert':
        sbert_model = SentenceTransformer('bert-base-nli-mean-tokens', cache_folder=cache_folder)

        document_embeddings = sbert_model.encode(documents)
        return document_embeddings
    
    if embedding == 'minilm':
        minilm = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', cache_folder=cache_folder)

        document_embeddings = minilm.encode(documents)
        return document_embeddings

    if embedding == 'tfidf':
        word_vectorizer = TfidfVectorizer(
            sublinear_tf=True, stop_words='english')
        word_vectorizer.fit(documents)
        word_features = word_vectorizer.transform(documents)

        return word_features
    
    # if embedding == 'distilbert':
    #     distilbert = SentenceTransformer('sentence-transformers/msmarco-distilbert-base-tas-b', cache_folder=os.path.join(os.getcwd(), 'embedding'))

    #     document_embeddings = distilbert.encode(documents)
    #     return document_embeddings

def load_model():
    """Load the model and nltk packages"""
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens', cache_folder=cache_folder)
    minilm = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', cache_folder=cache_folder)
    print('Embedding models are ready')
    return