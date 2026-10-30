import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/ask"

st.title("Document Q&A")
st.caption("Ask questions about the document. Answers cite page numbers.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if question := st.chat_input("Ask a question about the document"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the document..."):
            try:
                r = requests.post(API_URL, json={"question": question}, timeout=120)
                r.raise_for_status()
                data = r.json()
                pages = ", ".join(str(p) for p in data["pages"])
                reply = f"{data['answer']}\n\n*Sources: pages {pages}*"
            except Exception as e:
                reply = f"Something went wrong: {e}"
        st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})