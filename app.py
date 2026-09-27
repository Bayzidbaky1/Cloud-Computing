import os
import google.generativeai as genai
import streamlit as st

# Title & Info
st.title("AI Text Generator")
st.subheader("Name: Md. Bayzid Baki | Student ID: [Apnar Student ID Boshann]")

# Gemini API Key Configure
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# User Input
user_prompt = st.text_input("Enter your prompt / question:")

if st.button("Generate"):
    if not api_key:
        st.error("API Key paowa jayni! Render Environment Variable check korun.")
    elif user_prompt:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_prompt)
            st.write("### AI Response:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Doyakore kichu ekta likhun.")
