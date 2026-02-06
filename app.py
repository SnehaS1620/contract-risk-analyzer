import streamlit as st
import pandas as pd

from ingestion import extract_text
from clause_splitter import split_clauses
from risk_engine import analyze_clause
from llm_helper import explain_clause, summarize_contract
from report import create_pdf


# --------------------------------------------------
# Page setup
# --------------------------------------------------

st.set_page_config(page_title="AI Contract Risk Analyzer", layout="wide")

st.title("📜 AI Contract Risk Analyzer for SMEs")
st.info("This tool highlights risky clauses, explains them in simple language, and suggests safer alternatives.")


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def classify_contract(text):
    t = text.lower()

    if "employee" in t or "salary" in t:
        return "Employment Agreement"
    if "lease" in t or "rent" in t:
        return "Lease Agreement"
    if "vendor" in t or "service" in t:
        return "Vendor / Service Contract"
    if "partner" in t:
        return "Partnership Deed"

    return "General Contract"


SUGGESTIONS = {
    "Indemnity": "Limit indemnity only to direct losses.",
    "Unilateral Termination": "Add 30–60 days notice before termination.",
    "Auto Renewal": "Make renewal manual instead of automatic.",
    "IP Transfer": "Retain shared or joint IP ownership.",
    "Penalty": "Cap penalties to a reasonable fixed amount.",
    "Non Compete": "Reduce duration or geographic scope."
}


# --------------------------------------------------
# Controls
# --------------------------------------------------

lang = st.selectbox("🌐 Language", ["English", "Hindi"])
use_ai = st.checkbox("🤖 Enable AI explanations", value=True)


# --------------------------------------------------
# Demo button
# --------------------------------------------------

demo_text = None

if st.button("🚀 Load Demo Contract"):
    demo_text = """
1. Vendor may terminate this agreement at any time without notice.
2. Client shall indemnify and hold harmless the vendor against all losses.
3. This agreement automatically renews for one year.
4. All intellectual property created belongs exclusively to the vendor.
"""


file = st.file_uploader("Upload contract", type=["pdf", "docx", "txt"])


# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------

text = None

if demo_text:
    text = demo_text
elif file:
    text = extract_text(file)


if text:

    # --------------------------
    # Contract classification
    # --------------------------
    ctype = classify_contract(text)
    st.success(f"📂 Detected Contract Type: {ctype}")


    # --------------------------
    # Summary
    # --------------------------
    st.subheader("📘 Contract Summary")

    if use_ai:
        summary = summarize_contract(text, lang)
    else:
        summary = "AI disabled — summary skipped."

    st.write(summary)


    # --------------------------
    # Clause processing
    # --------------------------
    clauses = split_clauses(text)
    results = []

    for c in clauses:
        risk, types = analyze_clause(c["text"])

        explanation = ""

        if use_ai and risk != "Low":
            explanation = explain_clause(c["text"], types, lang)

        results.append({
            "id": c["id"],
            "text": c["text"],
            "risk": risk,
            "types": types,
            "explanation": explanation
        })


    # --------------------------
    # Sort risky first
    # --------------------------
    results = sorted(results, key=lambda x: {"High": 0, "Medium": 1, "Low": 2}[x["risk"]])


    # --------------------------
    # Metrics dashboard
    # --------------------------
    high = sum(1 for r in results if r["risk"] == "High")
    med = sum(1 for r in results if r["risk"] == "Medium")
    low = sum(1 for r in results if r["risk"] == "Low")

    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 High Risk", high)
    col2.metric("🟡 Medium Risk", med)
    col3.metric("🟢 Low Risk", low)


    # --------------------------
    # Overall risk score
    # --------------------------
    score_map = {"Low": 1, "Medium": 2, "High": 3}
    avg_score = sum(score_map[r["risk"]] for r in results) / len(results)

    if avg_score < 1.5:
        level = "Low Risk"
        st.success(f"Overall Contract Risk: 🟢 {level}")
    elif avg_score < 2.3:
        level = "Medium Risk"
        st.warning(f"Overall Contract Risk: 🟡 {level}")
    else:
        level = "High Risk"
        st.error(f"Overall Contract Risk: 🔴 {level}")


    # --------------------------
    # Clause view
    # --------------------------
    st.subheader("⚠️ Clause Risk Analysis")

    for r in results:

        color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}[r["risk"]]

        with st.expander(f"{color} Clause {r['id']} — {r['risk']}"):

            st.write(r["text"])

            if r["explanation"]:
                st.write("---")
                st.write(r["explanation"])

            # suggestions
            for t in r["types"]:
                if t in SUGGESTIONS:
                    st.warning(f"💡 Suggested fix: {SUGGESTIONS[t]}")


    # --------------------------
    # Export options
    # --------------------------
    st.subheader("📄 Export")

    if st.button("Generate PDF Report"):
        create_pdf(summary, results)
        with open("report.pdf", "rb") as f:
            st.download_button("Download PDF", f, "contract_report.pdf")


    df = pd.DataFrame(results)
    st.download_button(
        "⬇️ Download CSV Report",
        df.to_csv(index=False),
        "risk_report.csv"
    )
