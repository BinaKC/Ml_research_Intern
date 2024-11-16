import streamlit as st
from langchain_ollama import ChatOllama

# pip install -qU langchain-ollama
# pip install langchain
# pip install streamlit

st.title("History Enabled Chat Application with Ollama, Langchain and llama3.2:1b !!!")

with st.form("llm-form"):
    text = st.text_area("Enter your question or statement:")
    submit = st.form_submit_button("Submit")

def generate_response(input_text):
    model = ChatOllama(model="llama3.2:1b", base_url="http://localhost:11434/")

    response = model.invoke(input_text)

    return response.content

if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

if submit and text:
    with st.spinner("Generating response..."):
        response = generate_response(text)
        st.session_state['chat_history'].append({"user": text, "ollama": response})
        st.write(response)

st.write("## Chat History")
for chat in reversed(st.session_state['chat_history']):
    st.write(f"**User**: {chat['user']}")
    st.write(f"**Assistant**: {chat['ollama']}")
    st.write("---")
