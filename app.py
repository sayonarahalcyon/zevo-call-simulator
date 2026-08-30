import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ZEVO Support Call Simulator", page_icon="\U0001F4DE", layout="centered")

PERSONAS = {
    "derek": {
        "name": "Derek",
        "assistant_id": "40454b93-0209-44e2-9f75-e5edfd4af925",
        "label": "Derek â Lockout / grace period confusion",
        "desc": "Overdue on payment, confused about whether he's in a grace period, and how much he owes.",
    },
    "derekt": {
        "name": "Jason T.",
        "assistant_id": "b4638d74-4400-4f21-81a4-97a5f3470d2b",
        "label": "Jason T. â Payment extension / collections",
        "desc": "Behind on payment, wants a partial-payment extension so he isn't locked out.",
    },
    "marcust": {
        "name": "Marcus T.",
        "assistant_id": "a6f56391-e5d0-483d-9cd1-35bc5ccfde1d",
        "label": "Marcus T. â Surcharge / billing dispute",
        "desc": "Disputes a charge on his account, wants an itemized breakdown before paying more.",
    },
    "terrence": {
        "name": "Terrence",
        "assistant_id": "8bf90df3-0d9a-42b6-8a40-54e77c8268ad",
        "label": "Terrence â Host departure / vehicle swap",
        "desc": "Host is leaving the platform, needs a replacement vehicle fast â it's his income.",
    },
    "priya": {
        "name": "Priya",
        "assistant_id": "90b74b45-a781-4674-bfe9-36392551428a",
        "label": "Priya â Vehicle condition / mechanical dispute",
        "desc": "Vehicle has a mechanical issue and she was charged a damage fee she disputes.",
    },
}

VAPI_PUBLIC_KEY = "f9fb49f0-856f-4107-b05d-2291113ca60c"

st.title("ZEVO Support Call Simulator")
st.caption(
    "Pick a scenario, then use the call button in the bottom-right corner of the box below to start. "
    "This runs entirely in your browser over the internet â no phone, no app, works from anywhere. "
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


def build_widget_html(public_key: str, assistant_id: str, persona_name: str) -> str:
    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: transparent;
  }}
  #launcher {{
    position: fixed;
    bottom: 16px;
    right: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    background: #0b0b0c;
    color: #fff;
    border: none;
    border-radius: 999px;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(0,0,0,.25);
  }}
  #launcher .dot {{
    width: 8px; height: 8px; border-radius: 50%; background: #22c55e;
  }}
  #panel {{
    display: none;
    position: fixed;
    bottom: 16px;
    right: 16px;
    width: 320px;
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,.18);
    overflow: hidden;
    border: 1px solid #e5e7eb;
  }}
  #panel.open {{ display: block; }}
  #panel-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px;
    border-bottom: 1px solid #f0f1f3;
  }}
  #panel-header .title {{ font-size: 14px; font-weight: 700; color: #111; }}
  #panel-header .subtitle {{ font-size: 12px; color: #6b7280; margin-top: 2px; }}
  #close-btn {{
    border: none; background: none; cursor: pointer; font-size: 16px; color: #9ca3af; line-height: 1;
  }}
  #panel-body {{
    padding: 24px 16px 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 160px;
  }}
  #mic-circle {{
    width: 56px; height: 56px; border-radius: 50%;
    background: #f3f4f6;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 12px;
  }}
  #mic-circle.live {{ background: #dcfce7; }}
  #status-text {{
    font-size: 13px; color: #6b7280; text-align: center; margin-bottom: 12px; min-height: 32px;
  }}
  #transcript {{
    width: 100%;
    max-height: 90px;
    overflow-y: auto;
    font-size: 12px;
    color: #374151;
    background: #f9fafb;
    border-radius: 8px;
    padding: 8px;
    margin-bottom: 12px;
    display: none;
  }}
  #action-btn {{
    width: 100%;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    color: #fff;
    background: #16a34a;
  }}
  #action-btn.end {{ background: #dc2626; }}
  #action-btn:disabled {{ opacity: .6; cursor: default; }}
</style>
</head>
<body>

<button id="launcher"><span class="dot"></span>Talk with {persona_name}</button>

<div id="panel">
  <div id="panel-header">
    <div>
      <div class="title">Talk with {persona_name}</div>
      <div class="subtitle" id="subtitle">Click the microphone to start</div>
    </div>
    <button id="close-btn">&times;</button>
  </div>
  <div id="panel-body">
    <div id="mic-circle">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>
    </div>
    <div id="status-text">Click the start button to begin a conversation</div>
    <div id="transcript"></div>
    <button id="action-btn">Start</button>
  </div>
</div>

<script type="module">
  import Vapi from "https://esm.sh/@vapi-ai/web@2.1.5";

  const PUBLIC_KEY = "{public_key}";
  const ASSISTANT_ID = "{assistant_id}";

  const launcher = document.getElementById("launcher");
  const panel = document.getElementById("panel");
  const closeBtn = document.getElementById("close-btn");
  const actionBtn = document.getElementById("action-btn");
  const statusText = document.getElementById("status-text");
  const subtitle = document.getElementById("subtitle");
  const micCircle = document.getElementById("mic-circle");
  const transcriptEl = document.getElementById("transcript");

  let inCall = false;
  const vapi = new Vapi(PUBLIC_KEY);

  function addTranscriptLine(role, text) {{
    transcriptEl.style.display = "block";
    const line = document.createElement("div");
    line.style.marginBottom = "4px";
    line.innerHTML = "<strong>" + (role === "assistant" ? "{persona_name}" : "You") + ":</strong> " + text;
    transcriptEl.appendChild(line);
    transcriptEl.scrollTop = transcriptEl.scrollHeight;
  }}

  launcher.addEventListener("click", () => {{
    panel.classList.add("open");
  }});
  closeBtn.addEventListener("click", () => {{
    panel.classList.remove("open");
  }});

  vapi.on("call-start", () => {{
    inCall = true;
    subtitle.textContent = "In call";
    statusText.textContent = "Connected â start talking";
    micCircle.classList.add("live");
    actionBtn.textContent = "End Call";
    actionBtn.classList.add("end");
    actionBtn.disabled = false;
  }});

  vapi.on("call-end", () => {{
    inCall = false;
    subtitle.textContent = "Click the microphone to start";
    statusText.textContent = "Call ended. Click Start to talk again.";
    micCircle.classList.remove("live");
    actionBtn.textContent = "Start";
    actionBtn.classList.remove("end");
    actionBtn.disabled = false;
  }});

  vapi.on("message", (m) => {{
    if (m.type === "transcript" && m.transcriptType === "final") {{
      addTranscriptLine(m.role, m.transcript);
    }}
  }});

  vapi.on("error", (e) => {{
    statusText.textContent = "Something went wrong â please try again.";
    actionBtn.textContent = "Start";
    actionBtn.classList.remove("end");
    actionBtn.disabled = false;
    inCall = false;
  }});

  actionBtn.addEventListener("click", async () => {{
    if (inCall) {{
      vapi.stop();
      return;
    }}
    actionBtn.disabled = true;
    statusText.textContent = "Connecting...";
    try {{
      await vapi.start(ASSISTANT_ID);
    }} catch (err) {{
      statusText.textContent = "Failed to start â please try again.";
      actionBtn.disabled = false;
    }}
  }});
</script>
</body>
</html>
"""


widget_html = build_widget_html(VAPI_PUBLIC_KEY, persona["assistant_id"], persona["name"])

components.html(widget_html, height=650, scrolling=False)

st.caption("Internal ZEVO applicant testing tool. Calls are simulated customers for training purposes only. Switching scenarios reloads the call widget.")
