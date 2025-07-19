from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_cohere import CohereEmbeddings
from sentence_transformers import SentenceTransformer
# import os
from youtube_transcript import get_transcript
from dotenv import load_dotenv

load_dotenv()


class RAG:
    def __init__(self, txt_data):
        self.txt_data = txt_data
        self.vectorstore = None
        self.retriever = None
        # self.encoder = CohereEmbeddings(model='embed-english-v3.0', cohere_api_key=os.environ['COHERE_API_KEY'])
        self.embedding_model = HuggingFaceEmbeddings(
            model = 'all-MiniLM-L6-v2'
        )


    def _text_split(self):
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.create_documents([self.txt_data])
        return chunks

    def _create_embeddings_and_vectorstore(self, chunks):
        vectorstore = FAISS.from_documents(chunks, self.embedding_model)
        return vectorstore

    def _build_vectorstore(self):
        self.vectorstore = self._create_embeddings_and_vectorstore(self._text_split())

    def _build_retriever(self, k=3):
        if self.vectorstore is None:
            raise ValueError('VectorStore not built yet! Call _build_vectorstore() first.')
        self.retriever = self.vectorstore.as_retriever(search_kwargs={'k':k})

    def build_rag(self, k=3):
        self._build_vectorstore()
        self._build_retriever(k)

    def retrieve_vectors(self, query: str ):
        if self.vectorstore is None:
            raise ValueError("VectorStore not built yet! Call build_rag() first.")
        if self.retriever is None:
            raise ValueError("Retriever not built yet! Call build_rag() first.")
        results = self.retriever.invoke(query)
        return results

if __name__ == '__main__':
    print('Getting Transcript!!')
    context = get_transcript("Gfr50f6ZBvo")
    print('Transcript Loaded!')
    print('Downloading Embedding Model!!')
    rag = RAG(context)
    print('Building RAG vectors and vectorstores...')
    rag.build_rag()
    print('RAG setup succesfully!!')
    print(rag.retrieve_vectors('What is the video about?'))
