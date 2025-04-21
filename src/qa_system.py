from config import get_config
from src.file_utils import get_documents_to_index, save_file_hashes, load_conversation_history, save_conversation_history
from src.embedding import create_embedding_model
from src.llm import LLMInterface
from src.index_manager import IndexManager
from src.document_processor import DocumentProcessor

class SmartDocumentQA:
    """Smart document question answering system."""
    
    def __init__(self, config=None):
        """Initialize the QA system with given or default configuration."""
        # Load configuration
        self.config = config or get_config()
        self.data_dir = self.config["data_dir"]
        self.persist_dir = self.config["persist_dir"]
        self.file_hashes_path = self.config["file_hashes_path"]

        self.general_history_path = self.config["general_history_path"]
        self.source_history_path = self.config["source_history_path"]
        self.general_conversation_history = load_conversation_history(self.general_history_path)
        self.source_conversation_history = load_conversation_history(self.source_history_path)
        
        # Initialize components
        self.embed_model = create_embedding_model(self.config["embedding_model"])
        self.llm = LLMInterface(
            model_name=self.config["llm_model"],
            temperature=self.config["llm_temperature"]
        )
        
        # Set up document indexing
        documents_to_index, new_hashes = get_documents_to_index(
            self.data_dir, 
            self.file_hashes_path
        )
        
        index_manager = IndexManager(self.persist_dir, self.embed_model)
        self.index = index_manager.get_or_create_index(documents_to_index)
        
        # Save index and hashes if needed
        if documents_to_index:
            index_manager.save_index(self.index)
            save_file_hashes(self.file_hashes_path, new_hashes)
        
        # Initialize document processor
        self.document_processor = DocumentProcessor(self.index, self.embed_model)
    

    def ask_question(self, question):
        """Process a question with conversation context and return relevant answers and sources."""
        print(f"\n🤖 Asking: {question}")
        
        # 1. Build conversation-aware query for better retrieval
        recent_history = self.source_conversation_history[-3:] if len(self.source_conversation_history) >= 3 else self.source_conversation_history
        contextual_query = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in recent_history])
        contextual_query += f"\nQ: {question}\nA:"

        # 2. Search documents using the full context
        search_results = self.document_processor.search_documents(contextual_query)

        # 3. Generate source-based summary using the same context
        source_based_summary = self.llm.get_source_based_summary(
            question, 
            search_results["source_texts"]
        )
        
        # 4. Save to source conversation history
        self.source_conversation_history.append({"question": question, "answer": source_based_summary})
        save_conversation_history(self.source_history_path, self.source_conversation_history)
        
        # 5. Generate general answer (optional: use same context here too)
        general_answer = self.llm.get_general_answer(question)
        self.general_conversation_history.append({"question": question, "answer": general_answer})
        save_conversation_history(self.general_history_path, self.general_conversation_history)

        # 6. Compile result
        result = {
            "question": question,
            "general_answer": general_answer,
            "source_based_summary": source_based_summary,
            "source_info": search_results["source_info"],
            "documents_with_matches": list(search_results["documents_with_matches"]),
            "documents_with_no_matches": list(search_results["documents_with_no_matches"]),
            "avg_score": search_results["avg_score"],
            "search_duration": search_results["search_duration"],
            "total_documents": search_results["total_documents"],
        }

        return result
