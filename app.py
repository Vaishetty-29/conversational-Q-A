import streamlit as st
import cohere
from dotenv import load_dotenv
import os

# Set up Streamlit UI
st.set_page_config(page_title="Conversational Q&A Chatbot")
st.header("Hey, Let's Chat")

# Load environment variables from .env file (contains API keys)
load_dotenv()

# Initialize Cohere client with your API key from the environment variable
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(cohere_api_key)

# Initialize session state to store chat flow messages
if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        {"role": "system", "content": "You are a comedian AI assistant"}
    ]

# Function to get response from Cohere API
def get_cohere_response(question):
    # Append the user's question to the flow of messages
    st.session_state['flowmessages'].append({"role": "user", "content": question})

    # Prepare the message format for Cohere API
    prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state['flowmessages']])

    # Call the Cohere API to generate a response
    response = co.generate(
        model="xlarge",  # Choose the model, you can also try different ones (e.g., "large", "medium", etc.)
        prompt=prompt,
        max_tokens=150,  # Control the response length
        temperature=0.5  # Control randomness of the response
    )

    # Extract the content from the response and append to the flow
    answer = response.generations[0].text.strip()
    st.session_state['flowmessages'].append({"role": "assistant", "content": answer})

    return answer

# Text input for user question
input_question = st.text_input("Ask your question:", key="input")

# Button to submit the question
submit = st.button("Ask the question")

# If submit button is clicked, get response from Cohere API
if submit:
    if input_question:
        response = get_cohere_response(input_question)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please enter a question.")
