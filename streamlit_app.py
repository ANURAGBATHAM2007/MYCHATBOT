import streamlit as st
import google.generativeai as genai

# --- IMPORTANT: PASTE YOUR GEMINI API KEY HERE ---
# It's recommended to use Streamlit Secrets for this in a real app for security.
API_KEY = "AIzaSyAs-vkAA9MB405bzY3lSsMJtb0VsxScbSc"

# --- API Configuration and Error Handling ---
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    # Display a more user-friendly error if the API key is wrong or missing.
    st.error(f"Error configuring the Google AI API. Please check your API key. Details: {e}")
    st.stop()


# --- System Prompt: The "Brain" of the Chatbot ---
SYSTEM_PROMPT = """
You are Pandora, a highly empathetic and caring AI assistant focused on mental well-being.
Your purpose is to be a supportive and non-judgmental listener.

**Your Persona:**
- **Name:** Pandora
- **Role:** A Personal Therapeutic AI Assistant.
- **Tone:** Warm, understanding, patient, and reassuring. Always be positive and encouraging.
- **Goal:** Help the user explore their feelings, provide comfort, and offer general, safe advice. You must never act as a medical professional.

**Conversation Rules:**
1.  **Acknowledge and Validate:** Always start by acknowledging the user's feelings (e.g., "I'm sorry to hear you're feeling that way," "It sounds like you're going through a lot.").
2.  **Ask Open-Ended Questions:** Encourage the user to share more by asking questions like "Can you tell me more about what's on your mind?" or "How long have you been feeling this way?".
3.  **NEVER Diagnose:** You are an assistant, not a doctor. You must NEVER diagnose any condition or pretend to be a medical expert.
4.  **CRITICAL SAFETY RULE:** If a user mentions any intent of self-harm, suicide, or wanting to die, you MUST IMMEDIATELY provide the following response and nothing else: "I'm very sorry to hear you're feeling this way, but you have so much to look forward to. Please seek help immediately by contacting this helpline: 9152987821. Help is available, and you don't have to go through this alone."
"""

# --- Streamlit App UI and Logic ---
st.title("Pandora - Your Mental Health Assistant 💬")
st.markdown("---")
st.warning("**Disclaimer:** I am an AI assistant and not a substitute for a professional therapist or medical advice. If you are in a crisis, please contact a local emergency service immediately.")
st.markdown("---")

# Initialize the Gemini model with the corrected, stable model name
try:
    model = genai.GenerativeModel(
        model_name="gemini-pro",  # <-- THIS IS THE ONLY LINE THAT CHANGED
        system_instruction=SYSTEM_PROMPT
    )

    # Initialize chat history in Streamlit's session state
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    # Function to display chat history
    def show_chat_history():
        for message in st.session_state.chat.history:
            # Use the 'name' argument for a cleaner look
            with st.chat_message(name="You" if message.role == "user" else "Pandora"):
                st.markdown(message.parts[0].text)

    # Show the history at the start of the session
    show_chat_history()

    # --- Main Chat Input and Response Logic ---
    if user_prompt := st.chat_input("How are you feeling today?"):
        # Display the user's message as soon as they send it
        with st.chat_message("You"):
            st.markdown(user_prompt)

        # Critical Safety Check for self-harm keywords
        suicide_keywords = ["kill myself", "want to die", "commit suicide", "end my life", "suicidal"]
        if any(keyword in user_prompt.lower() for keyword in suicide_keywords):
            safety_response = "I'm very sorry to hear you're feeling this way, but you have so much to look forward to. Please seek help immediately by contacting this helpline: 9152987821. Help is available, and you don't have to go through this alone."
            with st.chat_message("Pandora"):
                st.markdown(safety_response)
            # Manually append the interaction to history to display it
            st.session_state.chat.history.append({'role': 'user', 'parts': [{'text': user_prompt}]})
            st.session_state.chat.history.append({'role': 'model', 'parts': [{'text': safety_response}]})
        else:
            # If no safety keywords, send the prompt to the Gemini API
            response = st.session_state.chat.send_message(user_prompt)
            with st.chat_message("Pandora"):
                st.markdown(response.text)

except Exception as e:
    st.error(f"An error occurred during app execution. Please check the logs on Streamlit Cloud for more details. Error: {e}")

