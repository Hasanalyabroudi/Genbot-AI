import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="AI Chatbot System", layout="centered", initial_sidebar_state="auto")

st.title("AI Chatbot System")
st.markdown("Enter your question below and click **Send** to receive a response.")

# Create a form for user input to avoid rerunning the entire script on each change
with st.form(key='chat_form'):
    user_query = st.text_input("Ask a question:")
    submit_button = st.form_submit_button(label="Send")

if submit_button:
    if user_query:
        with st.spinner("Generating response..."):
            try:
                # Send request to the backend API
                api_url = f"http://127.0.0.1:8000/generate_response/{user_query}"
                response = requests.get(api_url)
                
                if response.status_code == 200:
                    # Parse the JSON response from the API
                    data = response.json()
                    reply = data.get('reply', "No reply received from the API.")
                    st.success("Response received!")
                    
                    st.write(reply)
                    
                else:
                    st.error("Error: Unable to get response from the backend.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a question.")
