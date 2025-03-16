import streamlit as st  # Web app framework
import subprocess  # To run Ollama commands
import fitz  # PyMuPDF for rendering PDFs
import docx  # To process Word documents
from io import BytesIO

# ----------------------------- STEP 1: FUNCTION TO INTERACT WITH GEMMA 3:1B -----------------------------
def ask_legal_ai(query):
    """
    Function to interact with Ollama using Gemma 3:1B.
    """
    response = subprocess.run(
        ["ollama", "run", "gemma3:1b", query],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    return response.stdout.strip()

# ----------------------------- STEP 2: FUNCTION TO RENDER PDF FILE -----------------------------
def render_pdf(uploaded_file):
    """
    Renders PDF pages as images for preview.
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    images = []
    for page in doc:
        pix = page.get_pixmap()
        img = BytesIO()
        pix.pil_save(img, format="PNG")
        images.append(img)
    return images

# ----------------------------- STEP 3: FUNCTION TO RENDER DOCX FILE -----------------------------
def render_docx(uploaded_file):
    """
    Extracts text from DOCX for display.
    """
    doc = docx.Document(uploaded_file)
    content = "\n".join([para.text for para in doc.paragraphs])
    return content

# ----------------------------- STEP 4: FUNCTION TO GENERATE LEGAL BRIEFING -----------------------------
def generate_briefing(content):
    """
    Uses the AI model to summarize the legal document.
    """
    summary = ask_legal_ai(f"Summarize the following legal document: {content}")
    return summary

# ----------------------------- STEP 5: STREAMLIT WEB APP UI -----------------------------
st.set_page_config(page_title="⚖️ AI Legal Advisor", page_icon="⚖️", layout="wide")
st.sidebar.title("Navigation")

# Sidebar Navigation (Dynamic View Preview & Briefing Options)
menu_options = ["📂 Upload Document"]
uploaded_file = st.sidebar.file_uploader("📂 Upload a Legal Document (PDF or Word)", type=["pdf", "docx"])

if uploaded_file:
    menu_options.append("🖼️ View Preview")
    menu_options.append("📜 Briefing")

selected_option = st.sidebar.radio("Go to:", menu_options)

if selected_option == "📂 Upload Document":
    st.title("📂 Upload Your Legal Document")
    st.write("Upload a PDF or DOCX file for analysis.")
    
elif selected_option == "🖼️ View Preview":
    st.title("🖼️ Document Preview")
    file_type = uploaded_file.name.split('.')[-1]
    
    if file_type == "pdf":
        images = render_pdf(uploaded_file)
        for img in images:
            st.image(img.getvalue(), use_column_width=True)
    elif file_type == "docx":
        doc_content = render_docx(uploaded_file)
        st.text_area("📄 DOCX Preview:", doc_content, height=600)

elif selected_option == "📜 Briefing":
    st.title("📜 Legal Briefing")
    file_type = uploaded_file.name.split('.')[-1]
    
    if file_type == "pdf":
        pdf_text = "\n".join([page.get_text("text") for page in fitz.open(stream=uploaded_file.read(), filetype="pdf")])
        briefing = generate_briefing(pdf_text)
    elif file_type == "docx":
        doc_text = render_docx(uploaded_file)
        briefing = generate_briefing(doc_text)
    
    st.markdown(f"### 📑 AI-Generated Legal Briefing\n\n{briefing}")

# Disclaimer
st.markdown("**Disclaimer:** The generated legal summary may not be fully accurate. Always consult a legal professional.")