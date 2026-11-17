"""Working baseline chatbot with optional retrieval-augmented generation."""
import streamlit as st
from llm import ask_llm
from rag import retrieve, build_context  # Find documents and format them for the model.

st.title("Project VITAL — LLM + RAG Lab")
enable_rag = st.sidebar.toggle("Enable RAG")  # Let the user turn document retrieval on or off.
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):  # Show saved source names when the chat is redrawn.
            st.caption("Sources: " + ", ".join(msg["sources"]))  # List the retrieved filenames.
question = st.chat_input("Ask a question")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    sources = []  # Keep track of filenames to display with this answer.
    try:
        if enable_rag:  # Retrieve context only when the toggle is enabled.
            results = retrieve(question)  # Find the most relevant documents.
            sources = [name for name, _, _ in results]  # Extract their filenames.
            answer = ask_llm(question, build_context(results))  # Send the formatted context to the model.
        else:  # Keep the original chatbot behavior when RAG is disabled.
            answer = ask_llm(question)  # Ask the model without document context.
    except Exception as exc:
        answer = f"Ollama unavailable: {exc}"
    with st.chat_message("assistant"):
        st.write(answer)
        if sources:  # Only show a source list when documents were found.
            st.caption("Sources: " + ", ".join(sources))  # Display the retrieved filenames.
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})  # Save the answer and its sources.
