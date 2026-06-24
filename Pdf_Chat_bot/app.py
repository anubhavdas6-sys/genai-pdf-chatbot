import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables from .env file
load_dotenv()

# Ensure API key is configured
if not os.getenv("OPENAI_API_KEY"):
    st.error("Please set your OPENAI_API_KEY in the .env file.")
    st.stop()

# Streamlit UI Configuration
st.set_page_config(page_title="Enterprise PDF Chatbot", layout="wide")
st.title("🤖 Enterprise Knowledge Base Chatbot")
st.write("Upload a PDF document to extract information and ask questions.")

# Initialize session state for chat history and vector store
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# Sidebar for Document Ingestion
with st.sidebar:
    st.header("Document Ingestion")
    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner("Processing document... Parsing, chunking, and embedding..."):
            # Save uploaded file temporarily to disk for the loader
            temp_file_path = f"temp_{uploaded_file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                # 1. Load the PDF
                loader = PyPDFLoader(temp_file_path)
                docs = loader.load()
                
                # 2. Split text into chunks
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                final_documents = text_splitter.split_documents(docs)
                
                # 3. Create Vector Embeddings and store in Chroma DB
                embeddings = OpenAIEmbeddings()
                st.session_state.vector_store = Chroma.from_documents(
                    final_documents, embeddings, collection_name="pdf_knowledge_base"
                )
                
                st.success("Document successfully indexed! Ready to chat.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

# Main Chat Interface
if st.session_state.vector_store is None:
    st.info("Please upload a PDF document in the sidebar to activate the chatbot.")
else:
    # Display previous chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # Accept user input
    if user_query := st.chat_input("Ask a question about your document:"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        # Build the RAG Retrieval Chain
        retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        
        # System Prompt configuration to ensure grounded answers
        system_prompt = (
            "You are an expert assistant answering questions based strictly on the provided context.\n"
            "If you do not know the answer based on the context, say that you cannot find the answer. "
            "Do not make up facts.\n\n"
            "Context:\n{context}"
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        # Combine documents and create retrieval chain
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        # Generate Response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing document sources..."):
                response = rag_chain.invoke({"input": user_query})
                answer = response["answer"]
                st.markdown(answer)
                
                # Optional: Show which chunks were retrieved for full transparency
                with st.expander("View Source Context"):
                    for i, doc in enumerate(response["context"]):
                        st.caption(f"Source {i+1} (Page {doc.metadata.get('page', 'Unknown')}):")
                        st.write(doc.page_content)
                        
        st.session_state.chat_history.append({"role": "assistant", "content": answer})