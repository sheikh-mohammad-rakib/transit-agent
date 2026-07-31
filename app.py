import streamlit as st
import os
import random
from google import genai
from google.genai import types

# Page Config
st.set_page_config(page_title="Smart Transit Agent", page_icon="🚌", layout="wide")
st.title("🚌 AI Commuter Assistant")
st.caption("Powered by Gemma 4 & Google AI Studio")

# Fetch API Key securely
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

# --- LOCAL MOCK TOOLS ---
def check_waterlogging(area: str) -> str:
    """Checks if a city area has severe waterlogging or flooding."""
    flooded = ["bahaddarhat", "2 no. gate", "chawkbazar", "motijheel", "agrabad"]
    if any(loc in area.lower() for loc in flooded):
        return f"ALERT: High waterlogging in {area}. Small vehicles cannot pass easily."
    return f"STATUS: Roads in {area} are currently clear of severe flooding."

def estimate_pathao(pickup: str, dropoff: str) -> str:
    """Gets estimated fare and surge pricing for Pathao rides."""
    surge = random.choice([1.0, 1.2, 1.8])
    return f"Pathao Bike: ~{int(70 * surge)} BDT | Pathao CNG: ~{int(180 * surge)} BDT (Surge: {surge}x)"

tools = [check_waterlogging, estimate_pathao]

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("Where are you heading? (e.g., 'Going from CUET to Bahaddarhat in rain')"):
    if not api_key:
        st.error("Please provide an API Key in the sidebar or Secrets!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    client = genai.Client(api_key=api_key)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing routes & calling APIs..."):
            # Initial Gemma 4 Call
            response = client.models.generate_content(
                model='gemma-4-31b-it',
                contents=user_input,
                config=types.GenerateContentConfig(tools=tools, temperature=0.3)
            )

            # Sidebar Tool Debugger
            st.sidebar.subheader("🔍 Function Calling Inspector")

            if response.function_calls:
                for call in response.function_calls:
                    st.sidebar.info(f"**Triggered Tool:** `{call.name}`")
                    st.sidebar.json(call.args)

                    # Execute Tool
                    if call.name == "check_waterlogging":
                        res = check_waterlogging(**call.args)
                    elif call.name == "estimate_pathao":
                        res = estimate_pathao(**call.args)
                    else:
                        res = "Tool executed successfully."

                    st.sidebar.success(f"**Output:** {res}")

                    # Final Answer with Function Result
                    final_resp = client.models.generate_content(
                        model='gemma-4-31b-it',
                        contents=[
                            user_input,
                            response.candidates[0].content,
                            types.Part.from_function_response(name=call.name, response={"result": res})
                        ]
                    )
                    st.write(final_resp.text)
                    st.session_state.messages.append({"role": "assistant", "content": final_resp.text})
            else:
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})