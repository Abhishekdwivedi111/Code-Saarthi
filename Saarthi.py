import streamlit as st
import time
import os
import zipfile
from pathlib import Path
from streamlit.components.v1 import html
from agent.graph import agent

# =====================================================
# Page Config (MUST BE FIRST)
# =====================================================
st.set_page_config(
    page_title="Code Saarthi",
    page_icon="🧠",
    layout="wide"
)

st.markdown(
    """
    <style>
    /* Remove top padding added by Streamlit */
    .block-container {
        padding-top: 0.5rem !important;
    }

    /* Optional: reduce extra margin above first element */
    .main > div {
        padding-top: 0rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.markdown("""
<style>
/* Allow full width */
.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
    max-width: 100% !important;
}
                    
/* Make columns breathe */
section[data-testid="stSidebar"] {
    width: 380px;
}

/* Smooth wide layout */
[data-testid="column"] {
    padding: 0.5rem 1.5rem;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* Fix caret (typing cursor) visibility */
textarea {
    caret-color: #ffffff !important;  /* white caret */
}

/* Optional: ensure text is visible in light mode */
textarea::placeholder {
    color: rgba(229,231,235,0.65) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
textarea {
    caret-color: currentColor !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Remove Streamlit's default spacing */
.prompt-title {
    margin-bottom: 4px !important;
}

/* Pull textarea upward */
div[data-testid="stTextArea"] {
    margin-top: -8px !important;
}

/* Textarea appearance */
textarea {
    background: linear-gradient(145deg, #0f172a, #020617) !important;
    color: #e5e7eb !important;
    border-radius: 14px !important;
    border: 2px solid rgba(99,102,241,0.4) !important;
    padding: 1rem !important;
    caret-color: #ffffff !important; /* cursor visibility */
}

/* Focus glow */
textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 4px rgba(99,102,241,0.25) !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- RUN BUTTON ----------
st.markdown("""
<style>
div.stButton > button {
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    color: white;
    border-radius: 999px;
    font-weight: 600;
    font-size: 1.05rem;
    padding: 0.65rem 2rem;
    box-shadow: 0 10px 25px rgba(99,102,241,0.35);
    transition: all 0.2s ease-in-out;
}
div.stButton > button:hover {
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# Ctrl + Enter Support
# =====================================================
html("""
<script>
document.addEventListener("keydown", function(e) {
    if (e.ctrlKey && e.key === "Enter") {
        const buttons = window.parent.document.querySelectorAll("button");
        for (let btn of buttons) {
            if (btn.innerText.includes("Run Saarthi")) {
                btn.click();
                break;
            }
        }
    }
});
</script>
""")

# =====================================================
# Custom CSS (Dark + Light Safe)
# =====================================================
st.markdown("""
<style>

/* ================= GLOBAL LAYOUT ================= */
.block-container {
    padding-top: 1.2rem !important;
    max-width: 1200px;
}

/* ================= HERO ================= */
.hero {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    border-radius: 18px;
    padding: 2.2rem;
    color: white;
    margin-bottom: 1.5rem;
    text-align: center;
}

/* ================= CARDS ================= */
.card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.3rem;
    border: 1px solid #e5e7eb;
    margin-bottom: 1.2rem;
}

/* ================= STATUS PILL ================= */
.status-pill {
    display: inline-block;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
}

.waiting { background-color: #64748b; color: white; }
.running { background-color: #f97316; color: white; }
.done    { background-color: #22c55e; color: white; }
.error   { background-color: #ef4444; color: white; }

/* ================= RUN BUTTON ================= */
.run-btn {
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    color: white;
    border: none;
    border-radius: 999px;
    padding: 0.75rem 1.6rem;
    font-size: 1.05rem;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    transition: all 0.25s ease;
    box-shadow: 0 10px 25px rgba(99,102,241,0.35);
}

.run-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 35px rgba(34,211,238,0.45);
}

.run-btn:active {
    transform: scale(0.97);
}

.run-btn.disabled {
    background: #94a3b8;
    cursor: not-allowed;
    box-shadow: none;
}

/* Prompt highlight card */
.prompt-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(34,211,238,0.15));
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
}

            
            
/* Hint text */
.prompt-hint {
    font-size: 0.9rem;
    font-weight: 600;
    color: #6366f1;
}

/* =========================
   Textarea Styling
========================= */
textarea {
    background: linear-gradient(135deg, #0f172a, #1e293b) !important;
    border: 2px solid rgba(99,102,241,0.5) !important;
    border-radius: 16px !important;
    color: #e5e7eb !important;
    font-size: 1.05rem !important;
    padding: 1.2rem !important;
    min-height: 170px !important;
    transition: all 0.25s ease;

    /* 👇 animation hook */
    animation: pulseGlow 1.5s ease-out 1;
}

/* =========================
   Pulse Animation
========================= */
@keyframes pulseGlow {
    0% {
        box-shadow: 0 0 0 0 rgba(99,102,241,0.4);
    }
    70% {
        box-shadow: 0 0 0 12px rgba(99,102,241,0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(99,102,241,0);
    }
}

/* Focus glow */
textarea:focus {
    border-color: #6366f1 !important;
    box-shadow:
        0 0 0 4px rgba(99,102,241,0.35),
        0 12px 30px rgba(99,102,241,0.35) !important;
}

/* ================= LOGS ================= */
.log-container {
    background: #f8fafc;
    border-radius: 12px;
    padding: 0.75rem;
    height: 220px;
    overflow-y: auto;
    font-family: monospace;
    font-size: 0.85rem;
    color: #0f172a;
    border: 1px solid #e5e7eb;
}

/* Placeholder visibility fix */
textarea::placeholder {
    color: rgba(203, 213, 225, 0.65) !important; /* slate-300 */
    font-size: 0.95rem;
}

/* When focused, make placeholder slightly fade */
textarea:focus::placeholder {
    color: rgba(203, 213, 225, 0.4) !important;
}
            

/* ================= FILE OUTPUT ================= */
.file-box {
    background: #f1f5f9;
    border-radius: 8px;
    padding: 0.6rem;
    font-family: monospace;
    font-size: 0.85rem;
    margin-bottom: 0.3rem;
}

/* Reduce space below section headings */
h2 {
    margin-bottom: 0.4rem !important;
}

/* Also reduce space above textarea */
textarea {
    margin-top: 0.2rem !important;
}

textarea {
    color: #e5e7eb !important;
    background-color: #0f172a !important;
}

                        
.prompt-wrap {
    margin-top: -0.3rem;
}

h2 {
    margin-bottom: 0.4rem !important;
}
            
/* ================= FOOTER ================= */
.footer {
    color: #64748b;      /* 👈 IMPORTANT */
    opacity: 0.8;
    font-size: 0.8rem;
    margin-top: 2rem;
    text-align: center;
}


</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
.prompt-wrap {
    margin-top: -8px;
}

div[data-testid="stTextArea"] {
    margin-top: 0;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# Session State
# =====================================================
if "status" not in st.session_state:
    st.session_state.status = "Waiting"

if "logs" not in st.session_state:
    st.session_state.logs = []

if "start_time" not in st.session_state:
    st.session_state.start_time = None

# =====================================================
# Header
# =====================================================
st.markdown("""
<div class="hero">
    <h1>🧠 Code Saarthi</h1>
    <p>Describe your project idea and I’ll plan, structure & generate it intelligently.</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# Layout
# =====================================================
col_main, col_side = st.columns([2, 1], gap="medium")


# =====================================================
# MAIN COLUMN
# =====================================================
with col_main:
    # Tight heading (no extra margin)
    st.markdown(
        "<h3 class='prompt-title'>👇 Write What You Want to Build</h3>",
        unsafe_allow_html=True
    )

    user_prompt = st.text_area(
        label="Project description input",
        placeholder=(
            "Describe your project idea here...\n\n"
            "Examples:\n"
            "• Build a calculator using HTML, CSS & JS\n"
            "• Create a Python REST API"
        ),
        height=170,
        label_visibility="collapsed"
    )


    recursion_limit = st.slider(
        "🔁 Saarthi (Agent) recursion limit",
        10, 300, 100
    )
    # =====================================================
    # RUN AGENT SECTION
    # =====================================================

    # ---------- RUN BUTTON (ONLY ONE) ----------
    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        run_clicked = st.button(
            "🚀 Run Saarthi",
            type="primary",
            use_container_width=True
        )


    # UI placeholders (created once)
    progress = st.progress(0)
    status_text = st.empty()
    log_box = st.empty()

    # -----------------------------
    # Run Agent Logic
    # -----------------------------
    if run_clicked and user_prompt.strip():

        st.session_state.status = "Running"
        st.session_state.start_time = time.time()
        st.session_state.logs = []


        def log(msg):
            st.session_state.logs.append(msg)
            log_box.code("\n".join(st.session_state.logs), language="text")


        try:
            # STEP 1
            log("🧠 Planning project structure...")
            status_text.info("🧠 Planning project structure...")
            progress.progress(20)
            time.sleep(0.4)

            # STEP 2
            log("⚙️ Generating code & files...")
            status_text.info("⚙️ Generating code & files...")
            progress.progress(55)

            agent.invoke(
                {"user_prompt": user_prompt},
                {"recursion_limit": recursion_limit}
            )

            # STEP 3
            log("📦 Finalizing output...")
            status_text.info("📦 Finalizing output...")
            progress.progress(90)
            time.sleep(0.4)

            # DONE
            progress.progress(100)
            log("✅ Project generated successfully!")

            status_text.success("✅ Project generated successfully")
            st.session_state.status = "Completed"

            time.sleep(0.5)

            # Clean progress UI
            progress.empty()
            status_text.empty()

        except Exception as e:
            st.session_state.status = "Error"
            log(f"❌ Error: {str(e)}")
            progress.empty()
            status_text.error("❌ Saarthi failed")

# =====================================================
# SIDEBAR / RIGHT PANEL
# =====================================================
with col_side:
    st.markdown("### ⚙️ Saarthi Status")

    # -----------------------------
    # Safe status → CSS class map
    # -----------------------------
    status_map = {
        "Waiting": "waiting",
        "Running": "running",
        "Completed": "done",
        "Error": "error"
    }

    # Get current status safely
    current_status = st.session_state.get("status", "Waiting")
    status_class = status_map.get(current_status, "waiting")

    # Status pill
    st.markdown(
        f"""
        <span class="status-pill {status_class}">
            {current_status}
        </span>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------
    # Elapsed time
    # -----------------------------
    if st.session_state.get("start_time"):
        elapsed = int(time.time() - st.session_state.start_time)
        st.write(f"⏱️ **Elapsed:** {elapsed}s")

    # -----------------------------
    # Extra info for error state
    # -----------------------------
    if current_status == "Error":
        st.warning("Saarthi failed. Check logs for details.")


    # Live logo panel
    st.markdown("---")
    if st.session_state.status == "Running":
        st.markdown("### 🤖 Saarthi Activity")
        st.info("🧠 Saarthi is thinking...")
    else:
        st.markdown("### 🤖 Saarthi Activity")
        st.success("Idle")

    if st.session_state.start_time:
        elapsed = int(time.time() - st.session_state.start_time)
        st.write(f"⏱️ Elapsed: **{elapsed}s**")

    # # -----------------------------
    # # LIVE LOGS
    # # -----------------------------
    # st.markdown("---")
    # st.markdown("### 🧾 Live Logs")

    # if "logs" not in st.session_state:
    #     st.session_state.logs = []

    # log_html = "<br>".join(st.session_state.logs)

    # st.markdown(
    #     f"""
    #     <div class="log-container">
    #         {log_html if log_html else "Waiting for agent output..."}
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )


    # Generated Files
    st.markdown("---")
    from pathlib import Path
    import zipfile

    st.markdown("### 📁 Generated Output")

    gen_path = Path("generated_project")

    if gen_path.exists():
        files = list(gen_path.rglob("*"))

        if files:
            for f in files:
                if f.is_file():
                    st.markdown(f"📄 `{f.relative_to(gen_path)}`")

            # Create ZIP
            zip_path = "generated_project.zip"
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for f in files:
                    if f.is_file():
                        zipf.write(f, arcname=f.relative_to(gen_path))

            with open(zip_path, "rb") as f:
                st.download_button(
                    "⬇️ Download Generated Project",
                    f,
                    file_name="generated_project.zip",
                    use_container_width=True
                )
        else:
            st.info("Generated directory is empty.")
    else:
        st.warning("No generated project found yet.")

# =====================================================
# Footer
# =====================================================
st.markdown(
    "<div class='footer'>⚡ Code Saarthi — Agentic Engineering Assistant</div>",
    unsafe_allow_html=True
)

