import os
import google.generativeai as genai
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AI Text Generator", 
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for UI Enhancement
st.markdown("""
    <style>
    .main {
        padding: 2rem 1rem;
    }
    .stTextArea textarea {
        border-radius: 10px;
        font-size: 16px;
    }
    .response-card {
        background-color: #1E293B;
        border-left: 5px solid #3B82F6;
        padding: 20px;
        border-radius: 8px;
        margin-top: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stButton button {
        border-radius: 8px;
        font-weight: bold;
        height: 48px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Title & Student Information Header
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

# Action Button
if st.button("✨ Generate Response", type="primary"):
    if not api_key:
        st.error("⚠️ API Key not found! Please check GEMINI_API_KEY in Render Environment Variables.")
    elif user_prompt.strip():
        with st.spinner("🤖 AI is thinking... Please wait..."):
            try:
                # Active supported model auto-detection
                models_list = [
                    m.name for m in genai.list_models()
                    if 'generateContent' in m.supported_generation_methods
                ]
                
                # Exclude thinking/experimental raw models to prevent inner plan leaks
                valid_models = [m for m in models_list if "2.5" not in m and "2.0" not in m]
                selected_model = valid_models[0] if valid_models else models_list[0]
                
                # System Instruction to force direct & clean responses
                model = genai.GenerativeModel(
                    selected_model,
                    system_instruction="You are a helpful AI assistant. Provide direct, clean responses. Do not include your internal thinking, chain of thought, or reasoning plan."
                )
                
                response = model.generate_content(user_prompt)
                
                # Render Clean Output Card
                st.subheader("💡 Generated Response")
                with st.container():
                    st.markdown(f'<div class="response-card">', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                # Fallback to standard flash model if dynamic fetch fails
                try:
                    model = genai.GenerativeModel(
                        "gemini-1.5-flash",
                        system_instruction="You are a helpful AI assistant. Provide direct, clean responses without internal thinking steps."
                    )
                    response = model.generate_content(user_prompt)
                    
                    st.subheader("💡 Generated Response")
                    st.markdown(response.text)
                except Exception as fallback_error:
                    st.error(f"Error generating response: {fallback_error}")
    else:
        st.warning("Please enter a prompt before clicking generate.")
