import json
import streamlit as st

from extractor import read_document, extract_fields
from validator import validate
from router import route_claim


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="ClaimWise AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: #0b1120;
    }

    /* Remove excessive top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    /* Header */
    .hero {
        background: linear-gradient(135deg, #111c35, #172554);
        padding: 30px 35px;
        border-radius: 20px;
        border: 1px solid #263657;
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        font-size: 17px;
        color: #94a3b8;
    }

    .status {
        display: inline-block;
        margin-top: 15px;
        padding: 6px 14px;
        border-radius: 20px;
        background: #123c2d;
        color: #4ade80;
        font-size: 13px;
        font-weight: 600;
    }

    /* Section cards */
    .section-card {
        background: #111827;
        border: 1px solid #25324a;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 8px;
    }

    .section-description {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 15px;
    }

    /* Route cards */
    .route-card {
        padding: 25px;
        border-radius: 18px;
        margin: 15px 0 25px 0;
        border: 1px solid;
    }

    .route-title {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .route-reason {
        font-size: 15px;
        color: #cbd5e1;
    }

    .fast {
        background: #052e1c;
        border-color: #166534;
    }

    .manual {
        background: #172554;
        border-color: #1d4ed8;
    }

    .investigation {
        background: #3b1118;
        border-color: #991b1b;
    }

    .specialist {
        background: #302b05;
        border-color: #854d0e;
    }

    /* Metric cards */
    .metric-card {
        background: #111827;
        border: 1px solid #25324a;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }

    .metric-number {
        font-size: 30px;
        font-weight: 800;
        color: #f8fafc;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 13px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #080e1a;
        border-right: 1px solid #1e293b;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        min-height: 45px;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #111827;
        border-radius: 15px;
        padding: 10px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 12px;
        margin-top: 35px;
        padding-top: 20px;
        border-top: 1px solid #1e293b;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🛡️ ClaimWise AI</div>
        <div class="hero-subtitle">
            Autonomous Insurance Claims Processing Agent
        </div>
        <div class="hero-subtitle">
            FNOL extraction • Validation • Intelligent routing • Explainable decisions
        </div>
        <div class="status">● SYSTEM READY</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("## 🧠 Processing Pipeline")

    st.markdown(
        """
        **01 — Document Intake**  
        PDF / TXT FNOL

        ↓

        **02 — Information Extraction**  
        Policy, incident, claimant & asset data

        ↓

        **03 — Validation**  
        Missing & inconsistent fields

        ↓

        **04 — Routing Engine**  
        Business rules

        ↓

        **05 — Explainable Output**  
        JSON + reasoning
        """
    )

    st.divider()

    st.markdown("### 📋 Routing Rules")

    st.markdown(
        """
        🟢 **Fast-track**  
        Damage < ₹25,000

        🔵 **Manual review**  
        Mandatory field missing

        🔴 **Investigation Flag**  
        Fraud / inconsistent / staged

        🟡 **Specialist Queue**  
        Injury claim
        """
    )

    st.divider()

    st.caption("ClaimWise AI • Assessment Prototype")


# ---------------------------------------------------------
# UPLOAD SECTION
# ---------------------------------------------------------

st.markdown(
    """
    <div class="section-card">
        <div class="section-title">📄 FNOL Document Intake</div>
        <div class="section-description">
            Upload a First Notice of Loss document in PDF or TXT format.
        </div>
    """,
    unsafe_allow_html=True,
)

uploaded = st.file_uploader(
    "Upload FNOL document",
    type=["pdf", "txt"],
    label_visibility="collapsed",
)

st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# PROCESS DOCUMENT
# ---------------------------------------------------------

if uploaded:

    try:

        text = read_document(
            uploaded.name,
            uploaded.getvalue()
        )

        with st.expander("🔎 View extracted document text"):
            st.text(text)

        st.markdown("")

        process = st.button(
            "⚡ PROCESS CLAIM",
            type="primary",
            use_container_width=True,
        )

        if process:

            with st.spinner("Analyzing FNOL document..."):

                fields = extract_fields(text)

                missing, inconsistencies = validate(fields)

                route, reasoning = route_claim(
                    fields,
                    missing,
                    inconsistencies
                )

                result = {
                    "extractedFields": fields,
                    "missingFields": missing,
                    "recommendedRoute": route,
                    "reasoning": reasoning,
                }


            # -------------------------------------------------
            # ROUTE DISPLAY
            # -------------------------------------------------

            route_class = {
                "Fast-track": "fast",
                "Manual review": "manual",
                "Investigation Flag": "investigation",
                "Specialist Queue": "specialist",
            }.get(route, "manual")


            st.markdown(
                f"""
                <div class="route-card {route_class}">
                    <div class="route-title">
                        🎯 {route}
                    </div>
                    <div class="route-reason">
                        {reasoning}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


            # -------------------------------------------------
            # METRICS
            # -------------------------------------------------

            total_fields = len(fields)
            extracted_count = sum(
                value not in (None, "", [])
                for value in fields.values()
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-number">{extracted_count}</div>
                        <div class="metric-label">Fields Extracted</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-number">{len(missing)}</div>
                        <div class="metric-label">Missing Fields</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-number">{len(inconsistencies)}</div>
                        <div class="metric-label">Inconsistencies</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col4:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-number">{total_fields}</div>
                        <div class="metric-label">Required Fields</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


            st.markdown("")


            # -------------------------------------------------
            # VALIDATION
            # -------------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### 🔍 Validation")

                if missing:
                    st.error(
                        "Missing: " + ", ".join(missing)
                    )
                else:
                    st.success(
                        "✓ All mandatory fields are present"
                    )

            with col2:

                st.markdown("### ⚠️ Consistency Check")

                if inconsistencies:

                    for item in inconsistencies:
                        st.warning(item)

                else:
                    st.success(
                        "✓ No inconsistencies detected"
                    )


            # -------------------------------------------------
            # EXTRACTED DATA
            # -------------------------------------------------

            st.markdown("### 📊 Extracted Claim Information")

            st.json(fields)


            # -------------------------------------------------
            # FINAL JSON
            # -------------------------------------------------

            st.markdown("### 🧾 Final JSON Output")

            st.json(result)

            json_data = json.dumps(
                result,
                indent=2,
                ensure_ascii=False
            )

            st.download_button(
                "⬇️ Download Claim JSON",
                data=json_data,
                file_name="claim_result.json",
                mime="application/json",
                use_container_width=True,
            )


    except Exception as exc:

        st.error(
            f"Could not process the document: {exc}"
        )

else:

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">
                🚀 Ready to process
            </div>
            <div class="section-description">
                Upload an FNOL document above to begin automated
                claim extraction and routing.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        ClaimWise AI • Autonomous Insurance Claims Processing Agent<br>
        Built with Python • Streamlit • PyMuPDF • Explainable Rule Engine
    </div>
    """,
    unsafe_allow_html=True,
)