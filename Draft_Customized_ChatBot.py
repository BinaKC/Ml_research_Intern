from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
import time

# Set up model
model = ChatOllama(model="llama3.2:1b", base_url="http://localhost:11434/")

system_message = SystemMessagePromptTemplate.from_template(
    """You are an AI assistant for an event manager.
    Always start with a greeting, respond in a friendly,
    professional tone, and keep responses concise (under 100 words)
    unless the user requests a detailed explanation. Assist with planning, organizing, and managing event-related tasks and inquiries."""
)

# Initialize chat history
chat_history = []

# Define response generation function with timing
def generate_response(chat_history):
    start_time = time.time()  # Start timer
    chat_template = ChatPromptTemplate.from_messages(chat_history)
    chain = chat_template | model | StrOutputParser()
    response = chain.invoke({})
    end_time = time.time()  # End timer
    print(f"Response time: {end_time - start_time:.2f} seconds")  # Print response time
    return response

# Retrieve chat history with system message
def get_history():
    history = [system_message]
    for chat in chat_history:
        prompt = HumanMessagePromptTemplate.from_template(chat['user'])
        history.append(prompt)

        ai_message = AIMessagePromptTemplate.from_template(chat['assistant'])
        history.append(ai_message)
    return history

# Main function for chat interaction
def chat_application():
    print("Event Management Assistant Chat Application")
    print("Type 'exit' to quit.")
    print("=" * 50)
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        if user_input:
            # Append user message to chat history
            chat_history.append({'user': user_input, 'assistant': ""})

            # Generate response
            current_history = get_history()
            response = generate_response(current_history)

            # Append assistant's response to chat history
            chat_history[-1]['assistant'] = response

            # Display conversation
            print(f"Assistant: {response}")
            print("-" * 50)

# Run the chat application
if __name__ == "__main__":
    chat_application()
