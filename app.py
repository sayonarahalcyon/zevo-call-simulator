import streamlit as st

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

# The live call itself runs on GitHub Pages, not embedded here. Streamlit's
# components.html() always renders custom HTML inside a sandboxed srcdoc
# iframe, and srcdoc documents always report location.origin as the string
# "null". Vapi's SDK loads Daily.co's WebRTC engine underneath, which calls
# postMessage(..., window.location.origin) during setup — that throws when
# origin is "null", so the audio pipeline never finishes initializing even
# though the call session itself connects. This is a structural limitation
# of Streamlit's custom-component iframe, not something fixable in this
# app's code, so the call runs on a normal top-level page instead.
GITHUB_PAGES_BASE = "https://sayonarahalcyon.github.io/zevo-call-simulator/"

st.title("ZEVO Support Call Simulator")
st.caption(
    "Pick a scenario, then open the call simulator to start. It runs entirely in your "
    "browser over the internet — no phone, no app, works from anywhere. Allow microphone "
    "access when prompted."
)

key = st.selectbox(
    "Scenario",
    options=list(PERSONAS.keys()),
    format_func=lambda k: PERSONAS[k]["label"],
)
persona = PERSONAS[key]

st.info(persona["desc"])

call_url = f"{GITHUB_PAGES_BASE}?persona={key}"
st.link_button(f"Open call simulator — Talk with {persona['name']} ↗", call_url, use_container_width=True)

st.caption("Opens in a new tab. Internal ZEVO applicant testing tool. Calls are simulated customers for training purposes only.")
