from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def create_embedding_model(model_name):
    """Create and return a HuggingFace embedding model."""
    return HuggingFaceEmbedding(model_name=model_name)