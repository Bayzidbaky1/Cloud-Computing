import os
import google.generativeai as genai
import streamlit as st

# Page Config
st.set_page_config(page_title="AI Text Generator", page_icon="🤖")

# Header & Student ID
st.title("🤖 AI Text Generator")
st.subheader("Name: Md. Bayzid Baki | Student ID: 2026512816")

# Environment Variable theke Gemini API Key read
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# Input Box
user_prompt = st.text_area("Enter your prompt / question:", placeholder="Write something here...")

# Action Button
if st.button("Generate Response", type="primary"):
    if not api_key:
        st.error("API Key paowa jayni! Render Environment Variable-e GEMINI_API_KEY check korun.")
    elif user_prompt.strip():
        with st.spinner("AI is thinking..."):
            try:
                # Dynamic Model Finder: Auto-selects active generation model
                available_models = [
                    m.name for m in genai.list_models() 
                    if 'generateContent' in m.supported_generation_methods
                ]
                
                if available_models:
                    # Uses the top available model (e.g. models/gemini-1.5-flash or similar)
                    selected_model = available_models[0]
                    model = genai.GenerativeModel(selected_model)
                    response = model.generate_content(user_prompt)
                    
                    st.success("Generated Response:")
                    st.write(response.text)
                else:
                    st.error("No valid Gemini model available for content generation.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a prompt before clicking generate.")
