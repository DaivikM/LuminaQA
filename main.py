import os
import shutil
import logging
import argparse
from src.qa_system import SmartDocumentQA
from src.logger import Logger
from src.exception_handler import handle_exceptions
from config import get_config
from dotenv import load_dotenv
load_dotenv()


@handle_exceptions
def console_app():
    """Run the application in interactive console mode."""
    import logging

    logger = logging.getLogger(__name__)
    logger.info("Starting Smart Document QA System in console mode")

    # Initialize QA system
    qa_system = SmartDocumentQA()

    print("\n📘 Smart Document QA is ready!")
    print("Type your question below. Type 'x' or 'exit' to quit.\n")

    while True:
        question = input("❓ Your question: ").strip()
        if question.lower() in ["x", "exit"]:
            print("\n👋 Exiting Smart Document QA. Goodbye!\n")
            logger.info("User exited the application.")
            break
        elif not question:
            print("⚠️ Please enter a question or type 'x' to exit.")
            continue

        logger.info(f"Processing question: {question}")
        result = qa_system.ask_question(question)

        # Display results
        logger.info("Query completed, displaying results")
        print("\n---- FINAL OUTPUT ----\n")
        print(f"Question:\n{result['question']}\n")
        print(f"\nGeneral LLM Answer:\n{result['general_answer']}\n")
        print(f"\nSource-Based Summary:\n{result['source_based_summary']}\n")

        print(f"Documents with Relevant Content ({len(result['documents_with_matches'])}):")
        for i, src in enumerate(result["source_info"], 1):
            print(f"{i}. Document: {src['file']}, Page: {src['page']}, Score: {src['score']:.4f}")
            print(f"   Text: {src['text'][:100]}...\n")

        if result["documents_with_no_matches"]:
            print("Documents with No Relevant Content:")
            for doc in sorted(result["documents_with_no_matches"]):
                print(f"- {doc}")

        print("\n\n---- METRICS ----")
        print(f"Total documents searched: {result['total_documents']}")
        print(f"Relevant passages found: {len(result['source_info'])}")
        print(f"Average relevance score: {result['avg_score']:.4f}")
        print(f"Document search time: {result['search_duration']:.2f} seconds\n")


@handle_exceptions
def console_app():
    """Run the application in interactive console mode."""
    import logging

    logger = logging.getLogger(__name__)
    logger.info("Starting Smart Document QA System in console mode")

    # Initialize QA system
    qa_system = SmartDocumentQA()

    print("\n📘 Smart Document QA is ready!")
    print("Type your question below. Type 'x' or 'exit' to quit.\n")

    while True:
        question = input("❓ Your question: ").strip()
        if question.lower() in ["x", "exit"]:
            print("\n👋 Exiting Smart Document QA. Goodbye!\n")
            logger.info("User exited the application.")
            break
        elif not question:
            print("⚠️ Please enter a question or type 'x' to exit.")
            continue

        logger.info(f"Processing question: {question}")
        result = qa_system.ask_question(question)

        # Display results
        logger.info("Query completed, displaying results")
        print("\n---- FINAL OUTPUT ----\n")
        print(f"Question:\n{result['question']}\n")
        print(f"\nGeneral LLM Answer:\n{result['general_answer']}\n")
        print(f"\nSource-Based Summary:\n{result['source_based_summary']}\n")

        print(f"Documents with Relevant Content ({len(result['documents_with_matches'])}):")
        for i, src in enumerate(result["source_info"], 1):
            print(f"{i}. Document: {src['file']}, Page: {src['page']}, Score: {src['score']:.4f}")
            print(f"   Text: {src['text'][:100]}...\n")

        if result["documents_with_no_matches"]:
            print("Documents with No Relevant Content:")
            for doc in sorted(result["documents_with_no_matches"]):
                print(f"- {doc}")

        print("\n\n---- METRICS ----")
        print(f"Total documents searched: {result['total_documents']}")
        print(f"Relevant passages found: {len(result['source_info'])}")
        print(f"Average relevance score: {result['avg_score']:.4f}")
        print(f"Document search time: {result['search_duration']:.2f} seconds\n")


        
@handle_exceptions
def web_app():
    """Run the application in web mode."""
    logger = logging.getLogger(__name__)
    logger.info("Starting Smart Document QA Web Interface")

    # # Initialize QA system
    # SmartDocumentQA()
    
    # Import here to avoid unnecessary imports when running in console mode
    import app
    app.start_server()

if __name__ == "__main__":
    # # Load environment variables
    # load_environment_variables()
    config = get_config()

    # Path to the folder you want to delete
    folder_path = config["conversation_dir"]

    # Check if the folder exists
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    # Initialize logging
    Logger(
        log_dir=config["log_dir"],
        console_level=config["console_log_level"],
        file_level=config["file_log_level"]
    )
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Smart Document QA System')
    parser.add_argument('--web', action='store_true', help='Run in web mode')
    args = parser.parse_args()
    
    if args.web:
        web_app()
    else:
        console_app()