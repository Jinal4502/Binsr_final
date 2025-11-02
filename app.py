#!/usr/bin/env python3
import os
import subprocess
import streamlit as st
from pathlib import Path
import time

# ---------- PATH SETUP ----------
BASE_DIR = Path(__file__).resolve().parent
CHALLENGE_DIR = BASE_DIR / "binsr-challenge"
SRC_DIR = CHALLENGE_DIR / "src"
BONUS_DIR = BASE_DIR / "bonus"

INPUT_JSON = SRC_DIR / "inspection.json"
OUTPUT_TREC_PDF = CHALLENGE_DIR / "output" / "combined_report.pdf"
OUTPUT_BINSR_PDF = BONUS_DIR / "inspection_report_html.pdf"
BINSR_SCRIPT = BONUS_DIR / "inspection_report_html.py"

# ---------- STREAMLIT CONFIG ----------
st.set_page_config(page_title="Binsr Report Generator", page_icon="📋", layout="centered")
st.title("📋 Binsr Inspection Report Generator")

st.markdown("""
Upload your `inspection.json` (optional), then generate one or both reports below.
""")

# ---------- SESSION STATE ----------
if "generated_reports" not in st.session_state:
    st.session_state.generated_reports = []

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("📤 Upload inspection.json (optional)", type=["json"])

if uploaded_file:
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    with open(INPUT_JSON, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Uploaded `{uploaded_file.name}` to `{SRC_DIR}`")

# ---------- REPORT TYPE SELECTION ----------
st.subheader("Select what you want to generate:")
col1, col2 = st.columns(2)
with col1:
    gen_trec = st.checkbox(
        "🧱 Generate TREC Report (TypeScript)",
        value=st.session_state.get("gen_trec", False),
        key="checkbox_trec"
    )
with col2:
    gen_binsr = st.checkbox(
        "🧾 Generate Binsr Customized Report (HTML/PDF)",
        value=st.session_state.get("gen_binsr", True),
        key="checkbox_binsr"
    )

# Remember checkbox selections
st.session_state.gen_trec = gen_trec
st.session_state.gen_binsr = gen_binsr

# ---------- GENERATE BUTTON ----------
if st.button("🚀 Generate Selected Reports", key="generate_button"):
    with st.spinner("Generating... please wait ⏳"):
        start = time.time()
        st.session_state.generated_reports.clear()  # reset list

        try:
            # --- Binsr HTML/PDF ---
            if gen_binsr:
                subprocess.run(
                    ["python", str(BINSR_SCRIPT)],
                    check=True,
                    cwd=BONUS_DIR
                )
                if OUTPUT_BINSR_PDF.exists():
                    st.session_state.generated_reports.append(("Binsr Customized Report", OUTPUT_BINSR_PDF))

            # --- TREC TypeScript ---
            if gen_trec:
                subprocess.run(["pnpm", "i"], check=True, cwd=CHALLENGE_DIR)
                subprocess.run(["npx", "ts-node", "src/generate_report.ts"], check=True, cwd=CHALLENGE_DIR)
                if OUTPUT_TREC_PDF.exists():
                    st.session_state.generated_reports.append(("TREC Report", OUTPUT_TREC_PDF))

            elapsed = time.time() - start
            st.success(f"✅ {len(st.session_state.generated_reports)} report(s) generated in {elapsed:.2f} seconds.")

        except subprocess.CalledProcessError as e:
            st.error(f"❌ Command failed: {e}")
        except Exception as ex:
            st.error(f"❌ Unexpected error: {ex}")

# ---------- DOWNLOAD SECTION ----------
if st.session_state.generated_reports:
    st.markdown("### ⬇️ Download your reports")
    for label, pdf_path in st.session_state.generated_reports:
        if pdf_path.exists():
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label=f"Download {label}",
                    data=f,
                    file_name=pdf_path.name,
                    mime="application/pdf",
                    key=f"download_{label}"  # unique key per button
                )
