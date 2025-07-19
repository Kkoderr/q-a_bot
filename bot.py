from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from ragSys import RAG

class BotResponse(BaseModel):
    generated_response: str = Field(description="Proper generated response to user question.")
    context_used: str = Field(description="Context used in the generated response.")

class Bot:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
        self.rag_prompt = ChatPromptTemplate.from_messages([
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
        self.summary_prompt = PromptTemplate(
            template = 'Generate a short 40-50 words summary for a video transcript \n {transcript}',
            input_variables=['transcript']
        )

    def invoke_summary(self, video_transcript):
        chain = self.summary_prompt | self.llm
        result = chain.invoke({'transcript': video_transcript})
        return result.content


    def invoke_chat(self, question, rag_instance: RAG):
        relevant_vectors = rag_instance.retrieve_vectors(question)
        if not relevant_vectors:
            raise ValueError("No relevant vectors retrieved. Ensure RAG is built and data is loaded.")
        context = "\n".join(doc.page_content for doc in relevant_vectors)
        final_prompt = self.rag_prompt.format_messages(
            context = context,
            question = question
        )
        chat_llm = self.llm.with_structured_output(BotResponse)
        result = chat_llm.invoke(final_prompt)
        return result