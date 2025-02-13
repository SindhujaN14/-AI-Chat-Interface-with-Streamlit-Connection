# AI Chatbot with Streamlit

This project creates an AI-powered chatbot using **Streamlit** for the frontend and a **FastAPI backend** to handle the AI's responses. The chatbot allows users to interact with an assistant, sending messages and receiving replies from the AI.

## Features

- **Streamlit frontend**: Simple and intuitive interface to interact with the chatbot.
- **FastAPI backend**: Handles communication with the AI model and processes user input.
- **Message history**: Displays a chat history, allowing users to view the entire conversation.
- **Retry mechanism**: Retries the AI request up to 3 times if there is no response.

## Requirements

1. Python 3.x
2. Install the following dependencies using `pip`:
   - `streamlit`
   - `requests`
   
   You can install these by running:

   ```bash
   pip install streamlit requests
