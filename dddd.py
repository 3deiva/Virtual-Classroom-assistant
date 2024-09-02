"""
import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Retrieve the API key and MongoDB URI from environment variables
groq_api_key = os.getenv('GROQ_API_KEY')
mongo_uri = os.getenv('MONGO_URI')
port = os.getenv('PORT')

def main():
    st.title("Classroom Chatbot Assistant")

    # Add customization options to the sidebar
    st.sidebar.title('Select an LLM')
    model = st.sidebar.selectbox(
        'Choose a model',
        ['llama-3.1-70b-versatile']  # Example model
    )
    conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value=5)

    memory = ConversationBufferWindowMemory(k=conversational_memory_length)

    user_question = st.text_area("Ask a question:")

    # Session state variable
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    else:
        for message in st.session_state.chat_history:
            memory.save_context({'input': message['human']}, {'output': message['AI']})

    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq(
        groq_api_key=groq_api_key, 
        model_name=model
    )

    conversation = ConversationChain(
        llm=groq_chat,
        memory=memory
    )

    if user_question:
        response = conversation(user_question)
        message = {'human': user_question, 'AI': response['response']}
        st.session_state.chat_history.append(message)
        st.write("Chatbot:", response['response'])

if __name__ == "__main__":
    main()

"""

import subprocess
import json

def interact_with_ollama(conversation):
    # Define the prompt with instructions for extracting specific information
    prompt = f"""
    Extract the following information from the conversation text:

    1. Customer Requirements for a Car:
       - Car Type (Hatchback, SUV, Sedan)
       - Fuel Type
       - Color
       - Distance Travelled
       - Make Year
       - Transmission Type

    2. Company Policies Discussed:
       - Free RC Transfer
       - 5-Day Money Back Guarantee
       - Free RSA for One Year
       - Return Policy

    3. Customer Objections:
       - Refurbishment Quality
       - Car Issues
       - Price Issues
       - Customer Experience Issues (e.g., long wait time, salesperson behavior)

    Conversation:
    {conversation}

    Extracted Information:
    """

    try:
        # Start the Ollama process
        process = subprocess.Popen(
            ['ollama', 'run', 'llama3'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        # Send the prompt to the model
        stdout, stderr = process.communicate(input=prompt, timeout=180)  # Timeout set to 180 seconds

        # Handle the response
        if stderr:
            print("Error:", stderr)
            return None
        
        # Print the response
        print("Raw Output:", stdout)

        # Parse and format the output
        return format_output(stdout)

    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        print("Timeout Expired")
        print("Output:", stdout)
        print("Error:", stderr)
    except Exception as e:
        print(f"An error occurred: {e}")

def format_output(output):
    # Format the output as required
    # This is a placeholder function and should be adjusted according to the actual response format
    # Here we assume the response is a string that needs to be converted to JSON format
    try:
        # Load the output as JSON
        data = json.loads(output)
        return data
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON from the output.")
        return None

def read_file(file_path):
    try:
        # Open the file in read mode with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the entire content of the file
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
        return None
    except UnicodeDecodeError as e:
        print(f"Error: Unicode decoding failed - {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Path to the text file
    file_path = r'C:\Users\DEIVA RAJA\Downloads\conv4.txt'
    
    # Read the content of the file
    conversation_text = read_file(file_path)
    
    if conversation_text:
        # Interact with Ollama using the file content
        extracted_info = interact_with_ollama(conversation_text)
        if extracted_info:
            # Print the formatted output
            print("Formatted Extracted Information:", json.dumps(extracted_info, indent=4))
