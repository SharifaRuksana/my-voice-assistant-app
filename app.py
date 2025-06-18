# app.py
import streamlit as st
from groq import Groq 
from html import escape

api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# Load persona prompt
with open("persona_prompt.txt", "r") as f:
    system_prompt = f.read()

# Streamlit UI setup
st.set_page_config(page_title="Personal Voice Assistant", page_icon="🗣️", layout="centered")
st.title("Get to Know Me!")
st.markdown("Ask me anything about my background, skills, or experiences.")

# Text input
user_input = st.text_input("What would you like to know?")

if user_input:
    with st.spinner("Please wait while I gather my thoughts!"):
        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",  # Or use "llama3-70b-8192", etc.
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            reply = response.choices[0].message.content
            st.success("You have your answer! To hear it please click the button below.")

            st.markdown(f"**Answer:** {reply}")

            escaped_reply = escape(reply)

            st.components.v1.html(f"""
                <html>
                <body>
                    <button onclick="speak()">🔊 Click to hear! </button>

                    <script>
                    function speak() {{
                        var text = "{escaped_reply}";
                        var utterance = new SpeechSynthesisUtterance(text);
                        utterance.lang = 'en-US';
                        speechSynthesis.speak(utterance);
                    }}
                    </script>
                </body>
                </html>
            """, height=100)

        except Exception as e:
            st.error(f"Sorry, I encountered an error: {str(e)}")
