import sys
import tempfile
from pathlib import Path

# ==========================================================
# 1. PROJECT PATH CONFIGURATION
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ==========================================================
# 2. IMPORT LIBRARIES
# ==========================================================

import streamlit as st

from tutor.tutor_engine import ask_tutor
from rag.rag_pipeline import RAGPipeline
from rag.document_processor import process_pdf


# ==========================================================
# 3. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="NOVA AI Personal Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# 4. LOAD RAG PIPELINE
# ==========================================================

@st.cache_resource
def load_rag():
    return RAGPipeline()


# ==========================================================
# 5. SESSION STATE INITIALIZATION
# ==========================================================

defaults = {
    "messages": [],
    "chat_history": [],
    "started": False,
    "subject": "",
    "topic": "",
    "chat_mode": "AI Tutor",
    "uploaded_document_names": []
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# 6. APPLICATION HEADER
# ==========================================================

st.title("🎓 NOVA AI Personal Tutor")

st.markdown(
    """
    Your intelligent personal learning assistant powered by
    **Llama 3.2, Ollama, ChromaDB and Retrieval-Augmented Generation.**
    """
)

st.divider()


# ==========================================================
# 7. SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🎓 NOVA")

    st.caption("Your Personal AI Tutor")

    st.divider()

    st.subheader("💬 Learning Mode")

    selected_mode = st.radio(
        "Choose your learning mode:",
        ["AI Tutor", "Ask from PDF"],
        index=(
            0 if st.session_state.chat_mode == "AI Tutor"
            else 1
        )
    )

    if selected_mode != st.session_state.chat_mode:

        st.session_state.chat_mode = selected_mode
        st.session_state.messages = []
        st.session_state.chat_history = []

        st.rerun()

    st.divider()

    # ======================================================
    # AI TUTOR SETTINGS
    # ======================================================

    if st.session_state.chat_mode == "AI Tutor":

        st.subheader("📚 Start Learning")

        subject_input = st.text_input(
            "Enter Subject",
            placeholder="Artificial Intelligence"
        )

        topic_input = st.text_input(
            "Enter Topic",
            placeholder="Machine Learning"
        )

        if st.button(
            "🚀 Start Learning",
            use_container_width=True
        ):

            if not subject_input.strip() or not topic_input.strip():

                st.warning(
                    "Please enter both subject and topic."
                )

            else:

                st.session_state.subject = subject_input.strip()
                st.session_state.topic = topic_input.strip()

                st.session_state.messages = []
                st.session_state.chat_history = []

                first_question = (
                    f"Teach me {st.session_state.topic} "
                    f"in {st.session_state.subject} "
                    "from absolute beginner level. "
                    "Use simple explanations, practical examples, "
                    "real-world applications and understanding checks."
                )

                try:

                    with st.spinner(
                        "NOVA is preparing your personalized lesson..."
                    ):

                        answer = ask_tutor(
                            first_question,
                            []
                        )

                    st.session_state.chat_history = [
                        {
                            "role": "user",
                            "content": first_question
                        },
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    ]

                    st.session_state.messages = [
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    ]

                    st.session_state.started = True

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Unable to generate lesson: {error}"
                    )

    # ======================================================
    # PDF LEARNING SETTINGS
    # ======================================================

    else:

        st.subheader("📄 PDF Learning")

        st.write(
            "Upload your study materials and ask NOVA questions."
        )

        try:

            rag_instance = load_rag()

            st.success("RAG pipeline connected successfully!")

        except Exception as error:

            rag_instance = None

            st.error(
                f"RAG connection failed: {error}"
            )

    st.divider()

    # ======================================================
    # CLEAR CONVERSATION
    # ======================================================

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.started = False

        st.rerun()

    st.divider()

    st.caption("Powered by Ollama + Llama 3.2")


# ==========================================================
# 8. AI TUTOR MODE
# ==========================================================

if st.session_state.chat_mode == "AI Tutor":

    if not st.session_state.started:

        st.subheader("Welcome to NOVA! 👋")

        st.write(
            "Start your learning journey with your "
            "personal AI teaching assistant."
        )

        st.info(
            "Enter your subject and topic in the sidebar "
            "and click Start Learning."
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown("### 📚 Learn")

            st.write(
                "Understand difficult concepts "
                "from beginner to advanced level."
            )

        with col2:

            st.markdown("### 💡 Practice")

            st.write(
                "Learn through practical examples "
                "and real-world applications."
            )

        with col3:

            st.markdown("### 🎯 Improve")

            st.write(
                "Ask questions and improve your understanding."
            )

        st.divider()

        st.subheader("✨ NOVA Features")

        st.markdown("""
        - AI-powered personalized teaching
        - Interactive question answering
        - Beginner-friendly explanations
        - Practical examples
        - Real-world applications
        - Understanding-check questions
        """)

    else:

        st.subheader(
            f"📖 {st.session_state.subject}"
        )

        st.markdown(
            f"**Current Topic:** {st.session_state.topic}"
        )

        st.divider()

        # DISPLAY CHAT HISTORY

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):

                st.markdown(message["content"])

        # USER QUESTION

        user_question = st.chat_input(
            "Ask NOVA anything about your topic..."
        )

        if user_question:

            st.session_state.messages.append({
                "role": "user",
                "content": user_question
            })

            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            try:

                with st.spinner("NOVA is thinking..."):

                    response = ask_tutor(
                        user_question,
                        st.session_state.chat_history[:-1]
                    )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })

                st.rerun()

            except Exception as error:

                st.error(
                    f"NOVA encountered an error: {error}"
                )


# ==========================================================
# 9. PDF UPLOAD AND PROCESSING
# ==========================================================

else:

    st.subheader("📚 NOVA PDF Learning Center")

    st.write(
        "Upload your PDF study materials. NOVA will extract "
        "the content, create embeddings and store it in ChromaDB."
    )

    st.divider()

    # ------------------------------------------------------
    # PDF UPLOAD
    # ------------------------------------------------------

    st.subheader("📤 Upload Study Materials")

    uploaded_files = st.file_uploader(
        "Select your PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        help="You can select multiple PDF files."
    )

    if uploaded_files:

        st.write("### Selected Documents")

        for pdf_file in uploaded_files:

            st.write(
                f"📄 {pdf_file.name} "
                f"({pdf_file.size / 1024:.2f} KB)"
            )

    # ------------------------------------------------------
    # PROCESS PDF BUTTON
    # ------------------------------------------------------

    if st.button(
        "🚀 Upload and Process PDFs",
        use_container_width=True
    ):

        if not uploaded_files:

            st.warning(
                "Please select at least one PDF file."
            )

        else:

            try:

                rag_instance = load_rag()

                total_chunks = 0
                successful_files = 0

                progress_bar = st.progress(0)

                status_text = st.empty()

                # Temporary directory for uploaded PDFs

                with tempfile.TemporaryDirectory() as temp_dir:

                    for index, pdf_file in enumerate(uploaded_files):

                        status_text.info(
                            f"Processing: {pdf_file.name}"
                        )

                        # Save uploaded PDF temporarily.
                        # Keep its original filename.

                        safe_filename = Path(pdf_file.name).name

                        if not safe_filename.lower().endswith(".pdf"):
                            raise ValueError(
                                "Invalid PDF filename."
                            )

                        temporary_path = (
                            Path(temp_dir) / safe_filename
                        )

                        temporary_path.write_bytes(
                            pdf_file.getvalue()
                        )

                        # Extract text and metadata

                        chunks, metadata = process_pdf(
                            str(temporary_path)
                        )

                        if not chunks:

                            st.warning(
                                f"No readable text found in {pdf_file.name}."
                            )

                            progress_bar.progress(
                                (index + 1) / len(uploaded_files)
                            )

                            continue

                        # Ensure source metadata uses original filename

                        for item in metadata:

                            item["source"] = pdf_file.name

                        # Add document chunks to ChromaDB

                        rag_instance.vector_db.add_documents(
                            chunks,
                            metadata
                        )

                        total_chunks += len(chunks)

                        successful_files += 1

                        # Update progress

                        progress_bar.progress(
                            (index + 1) / len(uploaded_files)
                        )

                status_text.success(
                    "PDF processing completed!"
                )

                if successful_files:

                    st.success(
                        f"Successfully indexed {successful_files} PDF file(s)."
                    )

                    st.info(
                        f"Total text chunks added: {total_chunks}"
                    )

                    st.session_state.uploaded_document_names = list(
                        dict.fromkeys(
                            st.session_state.uploaded_document_names
                            + [
                                pdf.name for pdf in uploaded_files
                            ]
                        )
                    )

                else:

                    st.warning(
                        "No PDF documents were successfully indexed."
                    )

            except Exception as error:

                st.error(
                    f"PDF processing failed: {error}"
                )

    st.divider()

    # ------------------------------------------------------
    # INDEXED DOCUMENTS
    # ------------------------------------------------------

    st.subheader("📚 Knowledge Database")

    try:

        rag_instance = load_rag()

        document_count = (
            rag_instance.vector_db.get_database_count()
        )

        st.metric(
            "Indexed text chunks",
            document_count
        )

    except Exception as error:

        st.warning(
            f"Unable to retrieve database count: {error}"
        )

    st.divider()

    # ======================================================
    # 10. PDF QUESTION ANSWERING
    # ======================================================

    st.subheader("💬 Ask Questions From Your PDFs")

    st.write(
        "Ask questions about your indexed documents. "
        "NOVA retrieves relevant content and generates answers."
    )

    # DISPLAY PREVIOUS PDF MESSAGES

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if (
                message["role"] == "assistant"
                and message.get("sources")
            ):

                st.markdown("**📄 Source References**")

                for source in message["sources"]:

                    st.write(
                        f"📘 {source['source']} "
                        f"| Page {source['page']}"
                    )

    # QUESTION INPUT

    pdf_question = st.chat_input(
        "Ask a question about your indexed PDF documents..."
    )

    if pdf_question:

        st.session_state.messages.append({
            "role": "user",
            "content": pdf_question
        })

        try:

            with st.spinner(
                "NOVA is searching your documents..."
            ):

                rag_instance = load_rag()

                result = rag_instance.ask(
                    pdf_question
                )

            answer = result["answer"]

            sources = result["sources"]

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })

            st.rerun()

        except Exception as error:

            st.error(
                f"PDF question processing failed: {error}"
            )

    st.divider()

    st.caption(
        "NOVA uses ChromaDB, Nomic Embeddings and Llama 3.2."
    )