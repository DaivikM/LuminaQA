from flask import Flask, request, jsonify, render_template
import asyncio
import os
import logging
import time
from src.qa_system import SmartDocumentQA
from src.logger import Logger
from src.exception_handler import handle_exceptions
from threading import Thread
from config import get_config
from dotenv import load_dotenv
load_dotenv()

# Initialize the app
app = Flask(__name__, 
            static_folder="static",
            template_folder="templates")

# Load configuration
# load_environment_variables()
config = get_config()

# Initialize logging
Logger(
    log_dir=config["log_dir"],
    console_level=config["console_log_level"],
    file_level=config["file_log_level"]
)
logger = logging.getLogger(__name__)


# logger.info("Initializing QA system at startup...")
# qa_system = SmartDocumentQA()
# logger.info("QA system initialized")

# Initialize QA system
qa_system = None

def initialize_qa_system():
    global qa_system
    logger.info("Initializing QA system in background...")
    qa_system = SmartDocumentQA()
    logger.info("QA system initialized in background.")

# # Start background initialization
# Thread(target=initialize_qa_system, daemon=True).start() if qa_system is None else None

@app.route('/')
async def index():
    """Render the main page."""

    return render_template('index.html')

@app.route('/ask', methods=['POST'])
@handle_exceptions
def ask():
    """Handle user questions."""
    global qa_system
    
    # Initialize QA system if not already done
    if qa_system is None:
        logger.info("Initializing QA system...")
        qa_system = SmartDocumentQA()
        logger.info("QA system initialized")
        
    # Get question from request
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    logger.info(f"Processing question: {question}")
    start_time = time.time()
    
    # Process the question
    result = qa_system.ask_question(question)
    
    # Format response for UI
    response = {
        'question': result['question'],
        'general_answer': result['general_answer'],
        'source_based_summary': result['source_based_summary'],
        'sources': result['source_info'],
        'metrics': {
            'total_documents': result['total_documents'],
            'documents_with_matches': len(result['documents_with_matches']),
            'documents_with_no_matches': len(result['documents_with_no_matches']),
            'relevant_passages': len(result['source_info']),
            'avg_score': result['avg_score'],
            'search_duration': result['search_duration'],
            'total_duration': time.time() - start_time
        }
    }
    
    logger.info(f"Question processed in {time.time() - start_time:.2f} seconds")
    return jsonify(response)

@app.route('/status')
async def status():
    """Check system status."""
    global qa_system
    
    # Check if system is initialized
    system_ready = qa_system is not None
    
    # Get document stats if available
    doc_count = 0
    if system_ready and hasattr(qa_system.index, 'docstore'):
        docstore = qa_system.index.docstore.docs
        doc_count = len(set(doc.metadata.get('file_path', '') for doc in docstore.values() if 'file_path' in doc.metadata))
    
    return jsonify({
        'status': 'ready' if system_ready else 'initializing',
        'document_count': doc_count
    })

def start_server():
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        logger.info("Starting SmartDocumentQA Web Interface")
        Thread(target=initialize_qa_system, daemon=True).start() if qa_system is None else None
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    start_server()























# from flask import Flask, request, jsonify, render_template
# import os
# import logging
# import time
# from src.qa_system import SmartDocumentQA
# from src.logger import Logger
# from src.exception_handler import handle_exceptions
# from config import load_environment_variables, get_config

# # Initialize the app
# app = Flask(__name__, 
#             static_folder="static",
#             template_folder="templates")

# # Load configuration
# load_environment_variables()
# config = get_config()

# # Initialize logging
# Logger(
#     log_dir=config["log_dir"],
#     console_level=config["console_log_level"],
#     file_level=config["file_log_level"]
# )
# logger = logging.getLogger(__name__)

# # Initialize the QA system
# logger.info("Initializing QA system at startup...")
# qa_system = SmartDocumentQA()
# logger.info("QA system initialized")


# @app.route('/')
# def index():
#     """Render the main page."""
#     return render_template('index.html')

# @app.route('/ask', methods=['POST'])
# @handle_exceptions
# def ask():
#     """Handle user questions."""
#     global qa_system
        
#     # Get question from request
#     data = request.json
#     question = data.get('question', '')
    
#     if not question:
#         return jsonify({'error': 'No question provided'}), 400
    
#     logger.info(f"Processing question: {question}")
#     start_time = time.time()
    
#     # Process the question
#     result = qa_system.ask_question(question)
    
#     # Format response for UI
#     response = {
#         'question': result['question'],
#         'general_answer': result['general_answer'],
#         'source_based_summary': result['source_based_summary'],
#         'sources': result['source_info'],
#         'metrics': {
#             'total_documents': result['total_documents'],
#             'documents_with_matches': len(result['documents_with_matches']),
#             'documents_with_no_matches': len(result['documents_with_no_matches']),
#             'relevant_passages': len(result['source_info']),
#             'avg_score': result['avg_score'],
#             'search_duration': result['search_duration'],
#             'total_duration': time.time() - start_time
#         }
#     }
    
#     logger.info(f"Question processed in {time.time() - start_time:.2f} seconds")
#     return jsonify(response)

# @app.route('/status')
# def status():
#     """Check system status."""
#     global qa_system
    
#     # Check if system is initialized
#     system_ready = qa_system is not None
    
#     # Get document stats if available
#     doc_count = 0
#     if system_ready and hasattr(qa_system.index, 'docstore'):
#         docstore = qa_system.index.docstore.docs
#         doc_count = len(set(doc.metadata.get('file_path', '') for doc in docstore.values() if 'file_path' in doc.metadata))
    
#     return jsonify({
#         'status': 'ready' if system_ready else 'initializing',
#         'document_count': doc_count
#     })

# if __name__ == '__main__':
#     logger.info("Starting SmartDocumentQA Web Interface")
#     app.run(debug=True, host='0.0.0.0', port=5000)