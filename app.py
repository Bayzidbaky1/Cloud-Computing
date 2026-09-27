import os
import google.generativeai as genai
import streamlit as st

st.set_page_config(page_title="AI Text Generator", page_icon="🤖")

st.title("🤖 AI Text Generator")
st.subheader("Name: Md. Bayzid Baki | Student ID: 2026512816")

api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

user_prompt = st.text_area("Enter your prompt / question:", placeholder="Write something here...")

if st.button("Generate Response", type="primary"):
    if not api_key:
        st.error("API Key paowa jayni! Render Environment Variable-e GEMINI_API_KEY check korun.")
    elif user_prompt.strip():
        with st.spinner("AI is thinking..."):
            try:
                # Long-term stable model alias
                model = genai.GenerativeModel("gemini-1.5-flash-latest")
                response = model.generate_content(user_prompt)
                st.success("Generated Response:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a prompt before clicking generate.")
