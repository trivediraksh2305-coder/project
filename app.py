import streamlit as st
from openai import OpenAI

# --- INITIAL CONFIG ---
st.set_page_config(page_title="AI Creator Pro", page_icon="🤖", layout="centered")

# Initialize session state for the wizard and user data
if "step" not in st.session_state:
    st.session_state.step = 1
if "ai_config" not in st.session_state:
    st.session_state.ai_config = {}

# --- HELPER FUNCTIONS ---
def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

# --- UI DESIGN: MODERN WIZARD ---
st.title("🚀 Build Your Custom AI")

# Progress Bar
progress_text = f"Step {st.session_state.step} of 4"
st.progress(st.session_state.step / 4, text=progress_text)

# --- STEP 1: Basic Identity ---
if st.session_state.step == 1:
    st.header("Step 1: Who is this AI?")
    ai_name = st.text_input("Give your AI a name:", placeholder="e.g. Jarvis, Athena...")
    if st.button("Next ➡️", disabled=not ai_name):
        st.session_state.ai_config['name'] = ai_name
        next_step()

# --- STEP 2: Personality ---
elif st.session_state.step == 2:
    st.header("Step 2: Define Personality")
    tone = st.select_slider(
        "Select the AI's tone:",
        options=["Professional", "Friendly", "Sarcastic", "Hyper-Technical"]
    )
    if st.columns(2)[0].button("⬅️ Back"): prev_step()
    if st.columns(2)[1].button("Next ➡️"):
        st.session_state.ai_config['tone'] = tone
        next_step()

# --- STEP 3: Expertise ---
elif st.session_state.step == 3:
    st.header("Step 3: What is its superpower?")
    expertise = st.multiselect(
        "Select fields of expertise:",
        ["Coding", "Creative Writing", "Data Analysis", "Life Coaching", "Legal Advice"]
    )
    if st.columns(2)[0].button("⬅️ Back"): prev_step()
    if st.columns(2)[1].button("Launch AI 🚀", disabled=len(expertise) == 0):
        st.session_state.ai_config['expertise'] = expertise
        next_step()

# --- PHASE 2: THE AI CHAT INTERFACE ---
elif st.session_state.step == 4:
    config = st.session_state.ai_config
    st.success(f"✨ {config['name']} is online!")
    
    with st.sidebar:
        st.info(f"**Settings**\n\n- **Tone:** {config['tone']}\n- **Skills:** {', '.join(config['expertise'])}")
        if st.button("Reset Configuration"):
            st.session_state.step = 1
            st.rerun()

    # Chat Logic (Example using OpenAI)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": f"You are {config['name']}, a {config['tone']} assistant expert in {config['expertise']}."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask your AI anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # placeholder for AI logic
        with st.chat_message("assistant"):
            response = f"I am {config['name']}. You asked: '{prompt}'. (Connect your API key here!)"
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
