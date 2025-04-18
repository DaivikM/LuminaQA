import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from llama_index.core.retrievers import VectorIndexRetriever
from src.text_cleaner import TextCleaner

class DocumentProcessor:
    """Process documents for question answering."""
    
    def __init__(self, index, embed_model, cleaner=None):
        """Initialize with index and embedding model."""
        self.index = index
        self.embed_model = embed_model
        self.cleaner = cleaner or TextCleaner()
    
    def process_document(self, question, doc_path, retriever):
        """Process a single document for relevant content."""
        try:
            nodes = retriever.retrieve(question)
            relevant_nodes = [node for node in nodes if node.metadata.get("file_path") == doc_path]
            top_nodes = sorted(relevant_nodes, key=lambda n: getattr(n, "score", 0), reverse=True)[:2]

            results = []
            for node in top_nodes:
                cleaned_text = self.cleaner.clean_text(node.text)
                page = node.metadata.get("page_label") or node.metadata.get("page_number", "Unknown")
                results.append((doc_path, cleaned_text, page, getattr(node, "score", 0)))
            return doc_path, results
        except Exception as e:
            return doc_path, []
    
    def search_documents(self, question, top_k=50):
        """Search documents for relevant content to answer the question."""
        print("\n🚀 Searching documents concurrently...")
        start_time = time.time()
        
        retriever = VectorIndexRetriever(
            index=self.index, 
            similarity_top_k=top_k, 
            embed_model=self.embed_model
        )
        
        # Get all unique document paths
        docstore = self.index.docstore.docs if hasattr(self.index, 'docstore') else {}
        all_documents = set(doc.metadata.get('file_path', 'Unknown') for doc in docstore.values())
        
        # Initialize result variables
        source_info, source_texts = [], []
        documents_with_matches, documents_with_no_matches = set(), set()
        score_accumulator = []
        
        # Process documents concurrently
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [
                executor.submit(self.process_document, question, path, retriever) 
                for path in all_documents
            ]
            
            for future in as_completed(futures):
                doc_path, nodes = future.result()
                if nodes:
                    documents_with_matches.add(doc_path)
                    for doc, text, page, score in nodes:
                        source_info.append({
                            "file": doc, 
                            "text": text, 
                            "page": page, 
                            "score": score
                        })
                        source_texts.append(text)
                        score_accumulator.append(score)
                else:
                    documents_with_no_matches.add(doc_path)
        
        search_duration = time.time() - start_time
        print(f"✅ Search completed in {search_duration:.2f} seconds.")
        
        avg_score = sum(score_accumulator) / len(score_accumulator) if score_accumulator else 0
        
        return {
            "source_info": source_info,
            "source_texts": source_texts,
            "documents_with_matches": documents_with_matches,
            "documents_with_no_matches": documents_with_no_matches,
            "avg_score": avg_score,
            "search_duration": search_duration,
            "total_documents": len(all_documents),
        }