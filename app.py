import os
import requests
import streamlit as st

# Page Configuration
st.set_page_config(page_title="AI Text Generator", page_icon="🤖")

# Title & Student Information
st.title("🤖 AI Text Generator")
st.subheader("Name: Md. Bayzid | Student ID: 2026512816")

# Environment Variable theke Token neowa
HF_TOKEN = os.environ.get("HF_TOKEN")
API_URL = "https://router.huggingface.co/hf-inference/v1/chat/completions"

def query_huggingface(prompt):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/Llama-3.2-1B-Instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# UI Layout
user_prompt = st.text_area("Enter your prompt / question:", placeholder="Write something here...")

if st.button("Generate Response", type="primary"):
    if not HF_TOKEN:
        st.error("API Token Missing.")
    elif user_prompt.strip():
        with st.spinner("AI is thinking..."):
            try:
                output = query_huggingface(user_prompt)
                
                if "choices" in output and len(output["choices"]) > 0:
                    reply = output["choices"][0]["message"]["content"]
                    st.success("Generated Response:")
                    st.write(reply)
                elif "error" in output:
                    st.error(f"Hugging Face Error: {output['error']}")
                else:
                    st.write(output)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a prompt before clicking generate.")
