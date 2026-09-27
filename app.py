import os
import google.generativeai as genai
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AI Text Generator", 
    page_icon="🤖",
    layout="centered"
)

# Custom Styling for Clean Layout
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

def clean_response(text):
    """Internal thinking process ba plans filter kora"""
    if not text:
        return ""
    lines = text.strip().split("\n")
    clean_lines = []
    for line in lines:
        lower = line.lower().strip()
        if any(keyword in lower for keyword in ["the user said", "plan:", "acknowledge the greeting", "ask how i can help"]):
            continue
        clean_lines.append(line)
    return "\n".join(clean_lines).strip()

# Action Button
if st.button("✨ Generate Response", type="primary"):
    if not api_key:
        st.error("⚠️ API Key not found! Please check GEMINI_API_KEY in Render Environment Variables.")
    elif user_prompt.strip():
        with st.spinner("🤖 AI is thinking... Please wait..."):
            try:
                # Active supported models fetch kora
                all_models = [
                    m.name for m in genai.list_models()
                    if 'generateContent' in m.supported_generation_methods
                ]
                
                # 404 dewa models (2.5, 2.0, exp) filter out kora
                safe_models = [
                    m for m in all_models 
                    if not any(bad in m for bad in ["2.5", "2.0", "exp", "thinking"])
                ]
                
                # Safe model thakle oita use korbe, na thakle list-er flash/pro search korbe
                if safe_models:
                    selected_model = safe_models[0]
                else:
                    selected_model = "models/gemini-1.5-flash"
                
                model = genai.GenerativeModel(selected_model)
                
                # Direct Answer restrict kora System Prompt inline diye
                full_prompt = (
                    "You are a helpful assistant. Output ONLY the final direct response to the user. "
                    "Do NOT include internal reasoning, thinking, plans, or step-by-step notes.\n\n"
                    f"User: {user_prompt}"
                )
                
                response = model.generate_content(full_prompt)
                final_text = clean_response(response.text)
                
                st.subheader("💡 Generated Response")
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(final_text)
                    
            except Exception as e:
                # Ultimate fallback to gemini-1.5-flash
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(f"Answer directly: {user_prompt}")
                    final_text = clean_response(response.text)
                    
                    st.subheader("💡 Generated Response")
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(final_text)
                except Exception as fallback_err:
                    st.error(f"Error generating response: {fallback_err}")
    else:
        st.warning("Please enter a prompt before clicking generate.")
