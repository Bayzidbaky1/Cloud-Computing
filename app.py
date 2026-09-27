import os
import google.generativeai as genai
import streamlit as st

# Page Configuration
st.set_page_config(page_title="AI Text Generator", page_icon="🤖")

# Title & Student Information
st.title("🤖 AI Text Generator")
st.subheader("Name: Md. Bayzid Baki | Student ID: 2026512816")

# Environment Variable
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# UI Layout
user_prompt = st.text_area("Enter your prompt / question:", placeholder="Write something here...")

if st.button("Generate Response", type="primary"):
    if not api_key:
        st.error("API Key paowa jayni! Render Environment Variable-e GEMINI_API_KEY check korun.")
    elif user_prompt.strip():
        with st.spinner("AI is thinking..."):
            try:
                # Active supported models auto-detect
                models_list = [
                    m.name for m in genai.list_models()
                    if 'generateContent' in m.supported_generation_methods
                ]
                
                # Exclude expired models dynamically if listed
                valid_models = [m for m in models_list if "2.5" not in m and "2.0" not in m]
                
                selected_model = valid_models[0] if valid_models else models_list[0]
                
                model = genai.GenerativeModel(selected_model)
                response = model.generate_content(user_prompt)
                
                st.success("Generated Response:")
                st.write(response.text)
            except Exception as e:
                # Fallback to standard stable model if list_models fails
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(user_prompt)
                    st.success("Generated Response:")
                    st.write(response.text)
                except Exception as fallback_error:
                    st.error(f"Error: {fallback_error}")
    else:
        st.warning("Please enter a prompt before clicking generate.")
