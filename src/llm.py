from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

class LLMInterface:
    """Interface for language model interactions."""
    
    def __init__(self, model_name, temperature=0.3):
        """Initialize the LLM with specified parameters."""
        self.llm = ChatGroq(temperature=temperature, model_name=model_name)
    
    def get_response(self, prompt):
        """Get response from LLM for a given prompt."""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
    
    def get_source_based_summary(self, question, source_texts):
        """Generate a summary based on provided sources and question."""
        if not source_texts:
            return "No relevant content found."
            
        combined_texts = "\n\n".join(source_texts)
        prompt = f"""Based ONLY on the following text sources, provide a concise summary that answers the question: "{question}"

TEXT SOURCES:
{combined_texts}
"""
        return self.get_response(prompt)
    
    def get_general_answer(self, question):
        """Generate a general answer to the question without specific sources."""
        prompt = f"Answer this question generally: {question}"
        return self.get_response(prompt)