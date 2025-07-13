from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from ragSys import RAG

class BotResponse(BaseModel):
    generated_response: str = Field(description="Proper generated response to user question.")
    context_used: str = Field(description="Context used in the generated response.")

class Bot:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model='gemini-flash-2.0').with_structured_output(BotResponse)
        self.prompt = ChatPromptTemplate.from_messages([
            ('system', '''  
                        You are a helpful assistant.
                        Answer only from the provided transcript context.
                        If the context is insufficient, just say you don't know.
                        '''),
            ('system', """
                        Context: \n{context}
                        """),
            ('user', '{question}')
        ])

    def invoke(self, question, rag_instance: RAG):
        relevant_vectors = rag_instance.retrieve_vectors(question)
        if not relevant_vectors:
            raise ValueError("No relevant vectors retrieved. Ensure RAG is built and data is loaded.")
        context = "\n".join(doc.page_content for doc in relevant_vectors)
        final_prompt = self.prompt.format_messages(
            context = context,
            question = question
        )
        result = self.llm.invoke(final_prompt)
        return result