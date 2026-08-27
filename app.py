import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ZEVO Support Call Simulator", page_icon="\U0001F4DE", layout="centered")

PERSONAS = {
    "derek": {
        "name": "Derek",
        "assistant_id": "40454b93-0209-44e2-9f75-e5edfd4af925",
        "label": "Derek — Lockout / grace period confusion",
        "desc": "Overdue on payment, confused about whether he's in a grace period, and how much he owes.",
    },
    "derekt": {
        "name": "Jason T.",
        "assistant_id": "b4638d74-4400-4f21-81a4-97a5f3470d2b",
        "label": "Jason T. — Payment extension / collections",
        "desc": "Behind on payment, wants a partial-payment extension so he isn't locked out.",
    },
    "marcust": {
        "name": "Marcus T.",
        "assistant_id": "a6f56391-e5d0-483d-9cd1-35bc5ccfde1d",
        "label": "Marcus T. — Surcharge / billing dispute",
        "desc": "Disputes a charge on his account, wants an itemized breakdown before paying more.",
    },
    "terrence": {
        "name": "Terrence",
        "assistant_id": "8bf90df3-0d9a-42b6-8a40-54e77c8268ad",
        "label": "Terrence — Host departure / vehicle swap",
        "desc": "Host is leaving the platform, needs a replacement vehicle fast — it's his income.",
    },
    "priya": {
        "name": "Priya",
        "assistant_id": "90b74b45-a781-4674-bfe9-36392551428a",
        "label": "Priya — Vehicle condition / mechanical dispute",
        "desc": "Vehicle has a mechanical issue and she was charged a damage fee she disputes.",
    },
}

VAPI_PUBLIC_KEY = "f9fb49f0-856f-4107-b05d-2291113ca60c"

st.title("ZEVO Support Call Simulator")
st.caption(
    "Pick a scenario, then use the call button in the bottom-right corner of the box below to start. "
    "This runs entirely in your browser over the internet — no phone, no app, works from anywhere. "
    "Allow microphone access when prompted."
)

key = st.selectbox(
    "Scenario",
    options=list(PERSONAS.keys()),
    format_func=lambda k: PERSONAS[k]["label"],
)
persona = PERSONAS[key]

st.info(persona["desc"])
st.markdown(f"Click the **\"Talk with {persona['name']}\"** button in the bottom-right corner of the box below to start.")

widget_html = f"""
<!DOCTYPE html>
<html>
<head>
<script src="https://unpkg.com/@vapi-ai/client-sdk-react/dist/embed/widget.umd.js" async></script>
</head>
<body style="margin:0;">
<vapi-widget
  public-key="{VAPI_PUBLIC_KEY}"
  assistant-id="{persona['assistant_id']}"
  mode="voice"
  title="Talk with {persona['name']}"
></vapi-widget>
</body>
</html>
"""

components.html(widget_html, height=650, scrolling=False)

st.caption("Internal ZEVO applicant testing tool. Calls are simulated customers for training purposes only. Switching scenarios reloads the call widget.")
