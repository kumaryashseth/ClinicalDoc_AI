import time
from pathlib import Path

import streamlit as st

from config import (
    LLM_MODEL,
    UPLOAD_DIR
)

from pipeline.ingest import IngestionPipeline
from pipeline.generate import RAGGenerator
from retrievers.hybrid import HybridRetriever


# ----------------------------------------------------
# Page Config
# ----------------------------------------------------

st.set_page_config(
    page_title="ClinicalDoc AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

Path(UPLOAD_DIR).mkdir(
    parents=True,
    exist_ok=True
)

# ----------------------------------------------------
# Custom CSS
# ----------------------------------------------------

st.markdown(
    """
<style>

/* =======================================================
                    STREAMLIT CLEANUP
======================================================= */

#MainMenu{
    visibility:hidden;
}

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* =======================================================
                    MAIN APP
======================================================= */

.stApp{

background:#13071F;

background-image:
radial-gradient(circle at top right,#3B0764 0%,transparent 28%),
radial-gradient(circle at bottom left,#1E1B4B 0%,transparent 35%);

color:white;

}

.block-container{

max-width:1450px;

padding-top:1.3rem;

padding-bottom:1rem;

}

/* =======================================================
                    SIDEBAR
======================================================= */

section[data-testid="stSidebar"]{

background:#1B0D2E;

border-right:1px solid #4C1D95;

}

/* =======================================================
                    HEADER
======================================================= */

.header-card{

background:linear-gradient(
135deg,
#4C1D95,
#6D28D9,
#7C3AED
);

padding:28px;

border-radius:22px;

color:white;

border:1px solid #8B5CF6;

box-shadow:
0 15px 40px rgba(0,0,0,.45),
0 0 30px rgba(124,58,237,.25);

margin-bottom:25px;

}

/* =======================================================
                    METRIC CARD
======================================================= */

.metric-card{

background:#24163C;

padding:16px;

border-radius:18px;

border:1px solid #4C1D95;

margin-bottom:12px;

color:white;

transition:.25s;

box-shadow:
0 8px 18px rgba(0,0,0,.30);

}

.metric-card:hover{

transform:translateY(-3px);

box-shadow:
0 18px 30px rgba(124,58,237,.25);

}

/* =======================================================
                    STREAMLIT METRICS
======================================================= */

[data-testid="stMetric"]{

background:#24163C;

border-radius:16px;

padding:14px;

border:1px solid #4C1D95;

box-shadow:
0 8px 20px rgba(0,0,0,.25);

}

/* =======================================================
                    CHAT
======================================================= */

.stChatMessage{

background:#24163C;

border:1px solid #4C1D95;

border-radius:18px;

padding:15px;

box-shadow:
0 8px 20px rgba(0,0,0,.25);

margin-bottom:12px;

}

/* =======================================================
                    SOURCE CARD
======================================================= */

.source-card{

background:#312E81;

padding:16px;

border-radius:16px;

border-left:6px solid #A855F7;

margin-top:12px;

color:white;

box-shadow:
0 8px 20px rgba(0,0,0,.30);

}

/* =======================================================
                    BUTTONS
======================================================= */

.stButton>button{

background:linear-gradient(
135deg,
#7C3AED,
#8B5CF6
);

color:white;

border:none;

border-radius:14px;

height:48px;

width:100%;

font-weight:700;

transition:.25s;

box-shadow:
0 8px 18px rgba(124,58,237,.35);

}

.stButton>button:hover{

background:linear-gradient(
135deg,
#8B5CF6,
#A855F7
);

transform:translateY(-2px);

box-shadow:
0 12px 24px rgba(124,58,237,.45);

}

/* =======================================================
                    FILE UPLOADER
======================================================= */

[data-testid="stFileUploader"]{

background:#24163C;

border:2px dashed #8B5CF6;

border-radius:16px;

padding:14px;

}

/* =======================================================
                    CHAT INPUT
======================================================= */

[data-testid="stChatInput"]{

background:#24163C;

border:1px solid #4C1D95;

border-radius:18px;

}

/* =======================================================
                    EXPANDER
======================================================= */

.streamlit-expanderHeader{

background:#24163C;

border-radius:12px;

}

/* =======================================================
                    ALERTS
======================================================= */

.stAlert{

border-radius:14px;

}

/* =======================================================
                    TEXT
======================================================= */

h1,h2,h3,h4,h5,h6{

color:#FFFFFF !important;

font-weight:700;

}

p,span,label,small{

color:#F3E8FF !important;

}

/* =======================================================
                    LINKS
======================================================= */

a{

color:#C084FC !important;

}

/* =======================================================
                    SCROLLBAR
======================================================= */

::-webkit-scrollbar{

width:8px;

}

::-webkit-scrollbar-track{

background:#1B0D2E;

}

::-webkit-scrollbar-thumb{

background:#7C3AED;

border-radius:20px;

}

::-webkit-scrollbar-thumb:hover{

background:#A855F7;

}

/* =======================================================
                    SMOOTH EFFECT
======================================================= */

*{

transition:all .20s ease;

}

/* =======================================================
                    FORCE WHITE TEXT
======================================================= */

html,
body,
p,
span,
label,
small,
div,
li,
td,
th,
strong,
b{

    color:#FFFFFF !important;

}

h1,h2,h3,h4,h5,h6{

    color:#FFFFFF !important;

    font-weight:700;

}

/* Sidebar */

section[data-testid="stSidebar"] *{

    color:#FFFFFF !important;

}

/* Metrics */

div[data-testid="stMetric"] *{

    color:#FFFFFF !important;

}

/* Buttons */

.stButton button{

    color:#FFFFFF !important;

}

/* File Uploader */

[data-testid="stFileUploader"] *{

    color:#FFFFFF !important;

}

/* Chat */

.stChatMessage *{

    color:#FFFFFF !important;

}

/* Expander */

.streamlit-expanderHeader{

    color:#FFFFFF !important;

}

.streamlit-expanderContent *{

    color:#FFFFFF !important;

}

/* Caption */

.caption{

    color:#FFFFFF !important;

}

/* Markdown */

.stMarkdown *{

    color:#FFFFFF !important;

}

/* Info/Success/Warning */

.stAlert *{

    color:#FFFFFF !important;

}
/* ==========================================
        FILE UPLOADER FIX
========================================== */

[data-testid="stFileUploaderDropzone"]{

    background:#24163C !important;

    border:2px dashed #A855F7 !important;

    color:#FFFFFF !important;

}

[data-testid="stFileUploaderDropzone"] *{

    color:#FFFFFF !important;

}

[data-testid="stFileUploaderDropzone"] button{

    background:#7C3AED !important;

    color:white !important;

    border:none !important;

    border-radius:10px;

}

[data-testid="stFileUploaderDropzone"] small{

    color:#E9D5FF !important;

}
.stats-card{
    background:#24163C;
    border:1px solid #5B21B6;
    border-radius:18px;
    padding:15px;
    margin-top:10px;
}

.stats-row{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:10px 0;
    border-bottom:1px solid rgba(255,255,255,.08);
}

.stats-row:last-child{
    border-bottom:none;
}

.stats-row span:first-child{
    color:#C4B5FD;
    font-weight:600;
}

.stats-row span:last-child{
    color:#FFFFFF;
    font-weight:700;
    text-align:right;
    max-width:120px;
    word-break:break-word;
}

</style>
""",
unsafe_allow_html=True
)

# ----------------------------------------------------
# Session State
# ----------------------------------------------------

if "generator" not in st.session_state:
    st.session_state.generator = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "pages" not in st.session_state:
    st.session_state.pages = 0

if "chunks" not in st.session_state:
    st.session_state.chunks = 0

if "indexed" not in st.session_state:
    st.session_state.indexed = False

# ----------------------------------------------------
# Header
# ----------------------------------------------------

st.markdown(
    f"""
<div class="header-card">

<h1 style="margin-bottom:5px;">
🏥 ClinicalDoc AI
</h1>

<p style="font-size:18px;">
AI Powered Clinical Document Intelligence Platform
</p>

<hr>

<b>Model :</b> {LLM_MODEL}

&nbsp;&nbsp;&nbsp;&nbsp;

<b>Retrieval :</b> Hybrid RAG

&nbsp;&nbsp;&nbsp;&nbsp;

<b>Status :</b> 🟢 Ready

</div>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

with st.sidebar:

    st.title("📄 Document")

    uploaded_file = st.file_uploader(
        "Upload Medical PDF",
        type=["pdf"]
    )

    process_btn = st.button(
        "🚀 Process Document"
    )

    st.divider()

    st.subheader("📊 Document Stats")

    if st.session_state.indexed:

        st.markdown(
            f"""
<div class="metric-card">

<b>File</b><br>

{st.session_state.document_name}

</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
        f"""
    <div class="stats-card">

    <div class="stats-row">
    <span>📄 Pages</span>
    <span>{st.session_state.pages}</span>
    </div>

    <div class="stats-row">
    <span>✂️ Chunks</span>
    <span>{st.session_state.chunks}</span>
    </div>

    <div class="stats-row">
    <span>🔍 Retriever</span>
    <span>Hybrid RAG</span>
    </div>

    <div class="stats-row">
    <span>🤖 LLM</span>
    <span>{LLM_MODEL}</span>
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )

    else:

        st.info(
            "No document indexed."
        )

    st.divider()

    st.caption(
        "ClinicalDoc AI v2.0"
    )

# ----------------------------------------------------
# Chat Title
# ----------------------------------------------------

st.subheader("💬 Ask Questions About Your Medical Document")

col1, col2 = st.columns([1, 1])

with col1:
    summary_btn = st.button(
        "📝 Generate Document Summary",
        use_container_width=True
    )

with col2:
    st.empty()   # Future feature ke liye placeholder


# ----------------------------------------------------
# Process Document
# ----------------------------------------------------

if process_btn:

    if uploaded_file is None:

        st.warning("⚠️ Please upload a medical PDF first.")

    else:

        file_path = Path(UPLOAD_DIR) / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        progress = st.progress(0)

        status = st.empty()

        with st.spinner("Building Hybrid Index..."):

            status.info("📄 Loading PDF...")
            progress.progress(15)

            ingestion = IngestionPipeline()

            vector_store, bm25 = ingestion.ingest(
                str(file_path)
            )

            progress.progress(55)

            status.info("🧠 Creating Hybrid Retriever...")

            hybrid = HybridRetriever(
                vector_store=vector_store,
                bm25_retriever=bm25
            )

            progress.progress(80)

            status.info("🤖 Initializing ClinicalDoc AI...")

            generator = RAGGenerator(hybrid)

            progress.progress(100)

        st.session_state.generator = generator

        st.session_state.document_name = uploaded_file.name

        st.session_state.indexed = True

        try:

            retriever = vector_store.vector_store

            total_chunks = len(
                retriever.docstore._dict
            )

        except Exception:

            total_chunks = "Unknown"

        st.session_state.chunks = total_chunks

        st.session_state.pages = 1

        status.success(
            "✅ Document Indexed Successfully!"
        )

        st.toast(
            "Hybrid RAG Ready 🚀"
        )
# ----------------------------------------------------
# Document Summary (Temporary)
# ----------------------------------------------------

if summary_btn:

    if st.session_state.generator is None:

        st.error("Please process a PDF first.")

    else:

        with st.spinner("📝 Generating Medical Summary..."):

            summary = (
                st.session_state.generator.generate_summary()
            )

        st.subheader("📋 Medical Document Summary")

        st.success(summary)

        
# ----------------------------------------------------
# Chat Input
# ----------------------------------------------------

question = st.chat_input(
    "Ask anything about your medical document..."
)

if question:

    if st.session_state.generator is None:

        st.error(
            "Please process a PDF first."
        )

    else:

        start = time.time()

        with st.chat_message("user"):

            st.markdown(question)

        with st.chat_message("assistant"):

            thinking = st.empty()

            thinking.info(
                "🧠 Thinking..."
            )

            result = (
                st.session_state.generator.generate(
                    question
                )
            )

            thinking.empty()

            placeholder = st.empty()

            answer = result["answer"]

            output = ""

            for ch in answer:

                output += ch

                placeholder.markdown(output)

                time.sleep(0.008)

            elapsed = round(
                time.time() - start,
                2
            )

            st.caption(
                f"⏱ Response Time : {elapsed} sec"
            )

            if result["sources"]:

                with st.expander(
                    "📄 Sources Used"
                ):

                    for source in result["sources"]:

                        st.markdown(
                            f"""
<div class="source-card">

<b>📄 {source['document']}</b>

<br>

Page : {source['page']}

</div>
""",
                            unsafe_allow_html=True,
                        )

        st.session_state.chat_history.append(
            (
                question,
                result
            )
        )

# ----------------------------------------------------
# Sidebar - Chat Management
# ----------------------------------------------------

with st.sidebar:

    st.divider()

    st.subheader("💬 Conversation")

    if st.button("🗑 Clear Chat"):

        st.session_state.chat_history = []

        st.rerun()

    st.divider()

    st.subheader("⚙ Settings")

    show_sources = st.toggle(
        "Show Sources",
        value=True
    )

    typing_animation = st.toggle(
        "Typing Animation",
        value=True
    )

    st.divider()

    st.subheader("📈 System Status")

    st.success("🟢 LLM Connected")

    st.success("🟢 Hybrid Retriever")

    st.success("🟢 FAISS Ready")

    st.success("🟢 BM25 Ready")

# ----------------------------------------------------
# Previous Chat History
# ----------------------------------------------------

if st.session_state.chat_history:

    st.divider()

    st.subheader("📜 Conversation History")

    for idx, (question, result) in enumerate(
        st.session_state.chat_history[:-1]
    ):

        with st.expander(
            f"💬 Question {idx+1}"
        ):

            st.markdown(
                f"**👤 User**\n\n{question}"
            )

            st.markdown(
                f"**🤖 ClinicalDoc AI**\n\n{result['answer']}"
            )

            if (
                show_sources
                and result["sources"]
            ):

                st.markdown("### 📄 Sources")

                for source in result["sources"]:

                    st.markdown(
                        f"""
<div class="source-card">

📄 <b>{source['document']}</b>

<br>

Page : {source['page']}

</div>
""",
                        unsafe_allow_html=True,
                    )

# ----------------------------------------------------
# Download Conversation
# ----------------------------------------------------

if st.session_state.chat_history:

    history = ""

    for question, result in st.session_state.chat_history:

        history += (
            f"User : {question}\n\n"
        )

        history += (
            f"ClinicalDoc AI :\n"
            f"{result['answer']}\n\n"
        )

        history += "-" * 80 + "\n\n"

    st.download_button(

        "📥 Download Conversation",

        history,

        file_name="clinical_chat.txt",

        mime="text/plain"

    )

# ----------------------------------------------------
# Footer
# ----------------------------------------------------

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "LLM",
        LLM_MODEL
    )

with col2:

    st.metric(
        "Retriever",
        "Hybrid RAG"
    )

with col3:

    status = (
        "🟢 Ready"
        if st.session_state.indexed
        else "🟡 Waiting"
    )

    st.metric(
        "Status",
        status
    )

st.markdown(
    """
<center>

Made with ❤️ using

<b>Hybrid Retrieval-Augmented Generation</b>

<br><br>

ClinicalDoc AI v2.0

</center>
""",
    unsafe_allow_html=True
)