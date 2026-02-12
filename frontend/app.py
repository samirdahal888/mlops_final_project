import requests
import streamlit as st

# ─── Configuration ───────────────────────────────────────────────────────────

API_BASE_URL = "http://localhost:8000"

# ─── Page Setup ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="RAG Chat",
    page_icon="📄",
    layout="centered",
)

st.title("📄 RAG Chat Application")
st.caption("Upload documents and ask questions about them")

# ─── Session State ───────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []


# ─── API Client Functions ────────────────────────────────────────────────────


def index_document(uploaded_file) -> dict:
    """Send a file to the /index endpoint."""
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post(f"{API_BASE_URL}/index", files=files, timeout=120)
    response.raise_for_status()
    return response.json()


def ask_question(question: str, top_k: int = 5) -> dict:
    """Send a question to the /chat endpoint."""
    payload = {"question": question, "top_k": top_k}
    response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=120)
    response.raise_for_status()
    return response.json()


def check_health() -> dict:
    """Check if the backend is running."""
    response = requests.get(f"{API_BASE_URL}/health", timeout=10)
    response.raise_for_status()
    return response.json()


# ─── Sidebar: Backend Status & File Upload ───────────────────────────────────

with st.sidebar:
    st.header("⚙️ Settings")

    # Health check
    try:
        health = check_health()
        st.success(f"Backend: Connected")
        st.info(f"Indexed documents: {health['documents_count']} chunks")
    except Exception:
        st.error("Backend: Not connected. Is the server running?")

    st.divider()

    # File upload
    st.header("📁 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF or TXT file",
        type=["pdf", "txt"],
        help="Upload a document to index it for RAG",
    )

    if uploaded_file and st.button("📤 Index Document", use_container_width=True):
        with st.spinner(f"Indexing '{uploaded_file.name}'..."):
            try:
                result = index_document(uploaded_file)
                st.success(result["message"])
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Is the server running?")
            except requests.exceptions.HTTPError as e:
                st.error(f"Error: {e.response.text}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

    st.divider()

    # Settings
    top_k = st.slider(
        "Number of context chunks",
        min_value=1,
        max_value=20,
        value=5,
        help="How many relevant chunks to retrieve for each question",
    )

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ─── Chat Display ────────────────────────────────────────────────────────────

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    st.write(f"• {source}")


# ─── Chat Input ──────────────────────────────────────────────────────────────

if prompt := st.chat_input("Ask a question about your documents..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = ask_question(prompt, top_k=top_k)
                answer = result["answer"]
                sources = result.get("sources", [])

                st.markdown(answer)
                if sources:
                    with st.expander("📚 Sources"):
                        for source in sources:
                            st.write(f"• {source}")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )

            except requests.exceptions.ConnectionError:
                error_msg = "Cannot connect to backend. Is the server running?"
                st.error(error_msg)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_msg,
                    }
                )
            except Exception as e:
                error_msg = f"Error: {e}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_msg,
                    }
                )
