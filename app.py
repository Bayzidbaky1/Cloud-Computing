import os
import re
import google.generativeai as genai
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AI Text Generator", 
    page_icon="🤖",
    layout="centered"
)

# Custom Styling
st.markdown("""
    <style>
    .main { padding: 2rem 1rem; }
    .stTextArea textarea { border-radius: 10px; font-size: 16px; }
    .stButton button { border-radius: 8px; font-weight: bold; height: 48px; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.title("🤖 AI Text Generator")
st.caption("Cloud Computing Assignment | Render Deployment")
st.info("**Name:** Md. Bayzid Baki | **Student ID:** 2026512816")
st.divider()

# API Configuration
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# Input Section
user_prompt = st.text_area(
    "Enter your prompt or question below:", 
    placeholder="Ask me anything...", 
    height=120
)

def clean_ai_response(text):
    """Internal thinking, plans, and instructions strictly remove kora"""
    if not text:
        return ""
    
    # Remove lines containing thought/plan patterns
    lines = text.strip().split("\n")
    cleaned_lines = []
    
    for line in lines:
        lower_line = line.lower().strip()
        # Filter out system thoughts or planning lines
        if any(keyword in lower_line for keyword in ["the user said", "plan:", "acknowledge the greeting", "ask how i can help"]):
            continue
        cleaned_lines.append(line)
        
    result = "\n".join(cleaned_lines).strip()
    return result if result else text

# Action Button
if st.button("✨ Generate Response", type="primary"):
    if not api_key:
        st.error("⚠️ API Key not found! Please check GEMINI_API_KEY in Render Environment Variables.")
    elif user_prompt.strip():
        with st.spinner("🤖 AI is thinking... Please wait..."):
            try:
                # Dynamically fetch ALL models supporting generateContent
                available_models = [
                    m.name for m in genai.list_models()
                    if 'generateContent' in m.supported_generation_methods
                ]
                
                if not available_models:
                    st.error("No content generation models found for your API key.")
                else:
                    # Pick the first available model dynamically (No hardcoded names to avoid 404)
                    selected_model = available_models[0]
                    
                    model = genai.GenerativeModel(selected_model)
                    response = model.generate_content(
                        f"Provide ONLY the final direct answer to the user. Do not write any thoughts, plans, or reasoning steps.\n\nUser Question: {user_prompt}"
                    )
                    
                    raw_text = response.text if hasattr(response, 'text') else str(response)
                    final_output = clean_ai_response(raw_text)
                    
                    st.subheader("💡 Generated Response")
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(final_output)
                        
            except Exception as e:
                st.error(f"Error generating response: {e}")
    else:
        st.warning("Please enter a prompt before clicking generate.")
