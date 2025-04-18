import os
import logging
from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
    SimpleDirectoryReader
)
from src.exception_handler import handle_exceptions, IndexingError

logger = logging.getLogger(__name__)

class IndexManager:
    """Manager for document index operations."""
    
    def __init__(self, persist_dir, embed_model):
        """Initialize with storage directory and embedding model."""
        self.persist_dir = persist_dir
        self.embed_model = embed_model
        logger.debug(f"IndexManager initialized with persist_dir: {persist_dir}")
    
    @handle_exceptions
    def create_new_index(self, documents_to_index):
        """Create a new index from specified documents."""
        if not documents_to_index:
            logger.warning("No documents found to create index.")
            return VectorStoreIndex([], embed_model=self.embed_model)
            
        logger.info("Creating new index...")
        logger.info(f"Processing {len(documents_to_index)} documents...")
        
        try:
            reader = SimpleDirectoryReader(
                input_files=documents_to_index,
                file_metadata=lambda fname: {"file_path": fname}
            )
            documents = reader.load_data()
            logger.info(f"Loaded {len(documents)} document pages from {len(documents_to_index)} documents.")

            logger.info("Building index from documents...")
            index = VectorStoreIndex.from_documents(documents, embed_model=self.embed_model)
            logger.info("Index successfully built.")
            
            return index
        except Exception as e:
            raise IndexingError("Failed to create new index", e)
    
    @handle_exceptions
    def update_existing_index(self, index, documents_to_index):
        """Update existing index with new or changed documents."""
        if not documents_to_index:
            logger.info("No new/changed documents.")
            return index
            
        logger.info(f"Found {len(documents_to_index)} new/changed documents, updating index...")
        try:
            reader = SimpleDirectoryReader(
                input_files=documents_to_index,
                file_metadata=lambda fname: {"file_path": fname}
            )
            new_documents = reader.load_data()
            logger.info(f"Loaded {len(new_documents)} new/changed document pages from {len(documents_to_index)} documents.")

            logger.info("Inserting documents into the index...")
            for doc in new_documents:
                index.insert(doc)
            logger.info("Documents inserted successfully")
            
            return index
        except Exception as e:
            raise IndexingError("Failed to update existing index", e)
    
    @handle_exceptions
    def get_or_create_index(self, documents_to_index):
        """Load existing index or create new one if needed."""
        if os.path.exists(self.persist_dir):
            logger.info("Loading existing index...")
            try:
                storage_context = StorageContext.from_defaults(persist_dir=self.persist_dir)
                index = load_index_from_storage(storage_context, embed_model=self.embed_model)
                
                index = self.update_existing_index(index, documents_to_index)
            except Exception as e:
                raise IndexingError("Failed to load existing index", e)
        else:
            index = self.create_new_index(documents_to_index)
        
        return index
    
    @handle_exceptions
    def save_index(self, index):
        """Save index to persistent storage."""
        logger.info("Saving index to storage...")
        try:
            index.storage_context.persist(persist_dir=self.persist_dir)
            logger.info("Index successfully saved.")
        except Exception as e:
            raise IndexingError("Failed to save index", e)