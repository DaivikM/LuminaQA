from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from config import get_config
from src.file_utils import load_conversation_history

class LLMInterface:
    """Interface for language model interactions."""
    
    def __init__(self, model_name, temperature=0.3):
        """Initialize the LLM with specified parameters."""
        self.llm = ChatGroq(temperature=temperature, model_name=model_name)

        self.config = get_config()

        self.general_history_path = self.config["general_history_path"]
        self.source_history_path = self.config["source_history_path"]
    
    def get_response(self, prompt):
        """Get response from LLM for a given prompt."""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
    
    def get_source_based_summary(self, question, source_texts):
        """Generate a summary based on provided sources and question."""
        if not source_texts:
            return "No relevant content found."
        
        else:
            source_conversation_history = load_conversation_history(self.source_history_path)
            combined_texts = "\n\n".join(source_texts)

            if source_conversation_history:
                if len(source_conversation_history) > 10:
                    long_history = source_conversation_history[:-5]
                    recent_history = source_conversation_history[-5:]

                    summary_prompt = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in long_history])
                    summary_response = self.llm.invoke([
                        HumanMessage(content=f"Summarize this previous conversation:\n{summary_prompt}")
                    ])
                    history_summary = summary_response.content.strip()

                    source_context = (
                        f"Summary of earlier conversation:\n{history_summary}\n\n"
                        f"Recent conversation:\n" +
                        "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in recent_history])
                    )
                else:
                    source_context = "\n".join(
                        [f"Q: {qa['question']}\nA: {qa['answer']}" for qa in source_conversation_history]
                    )

                source_prompt = f"""
    Conversation so far:
    {source_context}

    Based ONLY on the following text sources, provide a concise summary that answers the question: "{question}"

    TEXT SOURCES:
    {combined_texts}
    """
            else:
                source_prompt = f"""
    Based ONLY on the following text sources, provide a concise summary that answers the question: "{question}"

    TEXT SOURCES:
    {combined_texts}
    """
    
        return self.get_response(source_prompt)
    
    def get_general_answer(self, question):
        """Generate a general answer to the question without specific sources."""
        # prompt = f"Answer this question generally: {question}"
        general_conversation_history = load_conversation_history(self.general_history_path)
        if general_conversation_history:
            general_context = "\n".join(
                [f"Q: {qa['question']}\nA: {qa['answer']}" for qa in general_conversation_history[-5:]]
            )
            combined_prompt = f"Conversation so far:\n{general_context}\nQ: {question}\nA:"
        else:
            combined_prompt = f"Q: {question}\nA:"
        return self.get_response(combined_prompt)