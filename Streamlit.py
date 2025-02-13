import streamlit as st
import requests
import time

def main():
    st.set_page_config(page_title="Chatbot", page_icon=":speech_balloon:", layout="centered")
    
    # Header
    st.title("AI Chatbot")
    st.markdown("Interact with an AI-powered assistant.")
    
    # Chat History
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User Input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Append user message to chat history
        st.session_state["messages"].append({"role": "user", "content": user_input})
        
        # Display user message in chat interface
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Send request to FastAPI backend
        api_url = "http://127.0.0.1:53140/chat"
        data = {"messages": st.session_state["messages"], "thread_id": "12345"}
        
        with st.spinner("AI is thinking..."):
            try:
                response = requests.post(api_url, json=data)
                response_json = response.json()

                # Extract final bot reply
                bot_reply = "No response from AI."

                if "response" in response_json and response_json["response"]:
                    # Loop through API response in reverse to find the last tool response
                    for event in reversed(response_json["response"]):
                        if "run_tool" in event and "messages" in event["run_tool"]:
                            messages = event["run_tool"]["messages"]
                            if messages and isinstance(messages, list):
                                bot_reply = messages[-1].get("content", "No content found.")
                                break  # Stop after finding the last tool response
                        elif "call_llm" in event and "messages" in event["call_llm"]:
                            # If LLM has a response, but it's not a tool call, use it
                            messages = event["call_llm"]["messages"]
                            if messages and isinstance(messages, list):
                                bot_reply = messages[-1].get("content", "No content found.")
                
                # Retry mechanism in case of no immediate response
                MAX_RETRIES = 3  
                for _ in range(MAX_RETRIES):
                    if bot_reply != "No response from AI.":
                        break
                    time.sleep(1)  # Wait a bit and try again

                # Append bot message to chat history
                st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
                
                # Display bot message in chat interface
                with st.chat_message("assistant"):
                    st.markdown(bot_reply)

            except requests.exceptions.RequestException as e:
                st.error("Failed to connect to the chatbot API.")
                st.text(str(e))

if __name__ == "__main__":
    main()
