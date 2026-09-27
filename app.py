import os
import google.generativeai as genai
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AI Text Generator", 
    page_icon="🤖",
    layout="centered"
)

# Custom Styling for Container
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
st.info("**Name:** Md. Bayzid | **Student ID:** 2026512816")
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
    """Thinking process ebong internal plan bad diye shudhu final response filter kora"""
    if not text:
        return ""
    
    # Plan: ba last sentence/paragraph clean kora
    lines = text.strip().split("\n")
    final_lines = []
    skip = False
    
    for line in lines:
        lower_line = line.lower()
        if "the user said" in lower_line or lower_line.startswith("plan:"):
            continue
        if lower_line.startswith("1.") or lower_line.startswith("2."):
            # Plan numbered items filter kora (jodi main sentence na hoy)
            if "acknowledge" in lower_line or "ask how" in lower_line:
                # Text-er moddhe actual answer thakle seta extract kora
                if "hello!" in lower_line or "hi!" in lower_line:
                    idx = line.lower().find("hello!")
                    if idx != -1:
                        final_lines.append(line[idx:])
                continue
        final_lines.append(line)
        
    result = "\n".join(final_lines).strip()
    return result if result else text

# Action Button
if st.button("✨ Generate Response", type="primary"):
    if not api_key:
        st.error("⚠️ API Key not found! Please check GEMINI_API_KEY in Render Environment Variables.")
    elif user_prompt.strip():
        with st.spinner("🤖 AI is thinking... Please wait..."):
            try:
                # Get available models
                models_list = [
                    m.name for m in genai.list_models()
                    if 'generateContent' in m.supported_generation_methods
                ]
                
                # Filter models to prioritize non-thinking stable versions
                valid_models = [m for m in models_list if "1.5" in m or "flash" in m]
                selected_model = valid_models[0] if valid_models else models_list[0]
                
                model = genai.GenerativeModel(
                    selected_model,
                    system_instruction="You are a polite AI assistant. Output ONLY the final response to the user. Do not include thinking process, reasoning steps, or plans."
                )
                
                response = model.generate_content(user_prompt)
                raw_text = response.text
                
                # Cleaning internal logs/thinking
                clean_text = clean_ai_response(raw_text)
                
                st.subheader("💡 Generated Response")
                
                # Modern Chat Message UI
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(clean_text)
                    
            except Exception as e:
                try:
                    # Fallback model
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(user_prompt)
                    clean_text = clean_ai_response(response.text)
                    
                    st.subheader("💡 Generated Response")
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(clean_text)
                except Exception as fallback_error:
                    st.error(f"Error generating response: {fallback_error}")
    else:
        st.warning("Please enter a prompt before clicking generate.")
