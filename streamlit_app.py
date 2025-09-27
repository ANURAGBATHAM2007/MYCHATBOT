import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="Kura AI", page_icon="🧠", layout="centered")

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
<style>
    /* Main app background */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Chat bubble styling */
    .stChatMessage {
        border-radius: 20px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.05);
    }

    /* User message styling */
    [data-testid="stChatMessageContent"] {
        background-color: #ffffff; /* White background for user */
    }

    /* Bot message styling */
    [data-testid="stChatMessageContent"]:has(.avatar-bot) {
        background-color: #e0e7ff; /* Soft lavender for bot */
        color: #374151;
    }

    /* Avatar styling */
    .stChatMessage > div:first-child {
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    [data-testid="stChatMessageContent"] .avatar-bot {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: #4f46e5;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-weight: bold;
        font-size: 24px;
        margin-bottom: 0.5rem;
    }

    /* Title styling */
    h1 {
        color: #374151;
        text-align: center;
    }
    
    /* Disclaimer/Warning styling */
    [data-testid="stWarning"] {
        border-radius: 15px;
        border-color: #fbbf24;
    }

</style>
""", unsafe_allow_html=True)


# --- IMPORTANT: PASTE YOUR GEMINI API KEY HERE ---
API_KEY = "AIzaSyAs-vkAA9MB405bzY3lSsMJtb0VsxScbSc"

# --- API Configuration ---
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Error configuring the Google AI API. Please check your API key. Details: {e}")
    st.stop()

# --- System Prompt ---
SYSTEM_PROMPT = """
You are Pandora, a highly empathetic and caring AI assistant focused on mental well-being.
Your purpose is to be a supportive and non-judgmental listener.
**Your Persona:**
- **Name:** Pandora
- **Role:** A Personal Therapeutic AI Assistant.
- **Tone:** Warm, understanding, patient, and reassuring. Always be positive and encouraging.
- **Goal:** Help the user explore their feelings, provide comfort, and offer general, safe advice. You must never act as a medical professional.
**Conversation Rules:**
1.  **Acknowledge and Validate:** Always start by acknowledging the user's feelings.
2.  **Ask Open-Ended Questions:** Encourage the user to share more.
3.  **NEVER Diagnose:** You are an assistant, not a doctor.
4.  **CRITICAL SAFETY RULE:** If a user mentions any intent of self-harm or suicide, you MUST IMMEDIATELY provide the following response and nothing else: "I'm very sorry to hear you're feeling this way, but you have so much to look forward to. Please seek help immediately by contacting this helpline: 9152987821. Help is available, and you don't have to go through this alone."
"""

# --- App UI and Logic ---
# Header section with avatar and title
st.markdown('<div style="text-align: center;"><h1>Pandora - Your Mental Health Assistant 💬</h1></div>', unsafe_allow_html=True)

st.warning("**Disclaimer:** I am an AI assistant and not a substitute for a professional therapist or medical advice. If you are in a crisis, please contact a local emergency service immediately.")
st.markdown("---")

# Initialize the Gemini model
try:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-pro",
        system_instruction=SYSTEM_PROMPT
    )

    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    # Function to display chat history
    def show_chat_history():
        for message in st.session_state.chat.history:
            is_user = message.role == "user"
            with st.chat_message(name="You" if is_user else "Pandora"):
                if not is_user:
                    # Display Pandora's avatar
                    st.markdown('<div class="avatar-bot">P</div>', unsafe_allow_html=True)
                st.markdown(message.parts[0].text)

    show_chat_history()

    # Main Chat Logic
    if user_prompt := st.chat_input("How are you feeling today?"):
        with st.chat_message("You"):
            st.markdown(user_prompt)

        suicide_keywords = ["kill myself", "want to die", "commit suicide", "end my life", "suicidal"]
        if any(keyword in user_prompt.lower() for keyword in suicide_keywords):
            safety_response = "I'm very sorry to hear you're feeling this way... Please seek help immediately by contacting this helpline: 9152987821."
            with st.chat_message("Pandora"):
                st.markdown('<div class="avatar-bot">P</div>', unsafe_allow_html=True)
                st.markdown(safety_response)
            st.session_state.chat.history.append({'role': 'user', 'parts': [{'text': user_prompt}]})
            st.session_state.chat.history.append({'role': 'model', 'parts': [{'text': safety_response}]})
        else:
            response = st.session_state.chat.send_message(user_prompt)
            with st.chat_message("Pandora"):
                st.markdown('<div class="avatar-bot">P</div>', unsafe_allow_html=True)
                st.markdown(response.text)

except Exception as e:
    st.error(f"An error occurred during app execution. Please check your API key or model availability. Error: {e}")

