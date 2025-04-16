from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

def create_chatbot(index, texts):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts, embeddings, index)
    chatbot = ConversationalRetrievalChain.from_llm(ChatOpenAI(model="gpt-3.5-turbo"), vectorstore.as_retriever())
    return chatbot

def chat_with_bot(query):
    response = chatbot({"question": query})
    return response['answer']
