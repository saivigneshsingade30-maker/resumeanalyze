import streamlit as st
import PyPDF2
from docx import Document

from resume_analyzer import analyze_resume


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# -----------------------------
# Custom CSS
# -----------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    color: #1f2937;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #6b7280;
    margin-bottom: 30px;
}

.score {
    font-size: 55px;
    font-weight: bold;
    text-align: center;
    color: #2563eb;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Extract PDF
# -----------------------------

def extract_pdf_text(file):
    reader = PyPDF2.PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# -----------------------------
# Extract DOCX
# -----------------------------

def extract_docx_text(file):
    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


# -----------------------------
# Extract Resume
# -----------------------------

def extract_resume_text(file):

    if file.name.lower().endswith(".pdf"):
        return extract_pdf_text(file)

    elif file.name.lower().endswith(".docx"):
        return extract_docx_text(file)

    else:
        return ""


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="title">📄 AI Resume Analyzer & ATS Optimizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload your resume and compare it with a job description'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("⚙️ Resume Analyzer")

    st.write(
        "This tool analyzes your resume and generates an ATS compatibility score."
    )

    st.markdown("---")

    st.write("Supported formats:")
    st.write("✅ PDF")
    st.write("✅ DOCX")


# -----------------------------
# Upload Resume
# -----------------------------

uploaded_file = st.file_uploader(
    "📤 Upload your Resume",
    type=["pdf", "docx"]
)


# -----------------------------
# Job Description
# -----------------------------

job_description = st.text_area(
    "💼 Paste Job Description",
    height=250,
    placeholder=(
        "Example:\n\n"
        "We are looking for a Python Developer with "
        "experience in Django, REST API, SQL, Git and AWS..."
    )
)


# -----------------------------
# Analyze Button
# -----------------------------

if st.button(
    "🚀 Analyze Resume",
    use_container_width=True
):

    if uploaded_file is None:

        st.error("Please upload your resume.")

    elif not job_description.strip():

        st.error("Please enter the job description.")

    else:

        with st.spinner("🤖 AI is analyzing your resume..."):

            try:

                resume_text = extract_resume_text(
                    uploaded_file
                )

                if not resume_text.strip():

                    st.error(
                        "Could not extract text from the resume."
                    )

                else:

                    result = analyze_resume(
                        resume_text,
                        job_description
                    )

                    st.success(
                        "Resume analysis completed successfully!"
                    )

                    st.markdown("---")

                    # -----------------------------
                    # ATS Score
                    # -----------------------------

                    st.subheader("🎯 ATS Compatibility Score")

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "ATS Score",
                            f"{result['ats_score']}%"
                        )

                    with col2:

                        st.metric(
                            "Keyword Match",
                            f"{result['keyword_score']}%"
                        )

                    with col3:

                        st.metric(
                            "Skills Found",
                            len(result["skills"])
                        )


                    # Progress bar

                    st.progress(
                        int(result["ats_score"])
                    )


                    # -----------------------------
                    # Contact information
                    # -----------------------------

                    st.markdown("---")

                    st.subheader("📞 Contact Information")

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"📧 Email: **{result['email']}**"
                        )

                    with col2:

                        st.write(
                            f"📱 Phone: **{result['phone']}**"
                        )


                    # -----------------------------
                    # Skills
                    # -----------------------------

                    st.markdown("---")

                    st.subheader("🛠️ Skills Detected")

                    if result["skills"]:

                        skills_text = " • ".join(
                            result["skills"]
                        )

                        st.info(skills_text)

                    else:

                        st.warning(
                            "No recognized technical skills found."
                        )


                    # -----------------------------
                    # Missing Keywords
                    # -----------------------------

                    st.markdown("---")

                    st.subheader(
                        "🔍 Missing Keywords"
                    )

                    if result["missing_keywords"]:

                        for keyword in result[
                            "missing_keywords"
                        ]:

                            st.write(
                                f"❌ {keyword}"
                            )

                    else:

                        st.success(
                            "No major missing keywords detected."
                        )


                    # -----------------------------
                    # Suggestions
                    # -----------------------------

                    st.markdown("---")

                    st.subheader(
                        "💡 Resume Improvement Suggestions"
                    )

                    for suggestion in result[
                        "suggestions"
                    ]:

                        st.write(
                            f"✅ {suggestion}"
                        )


                    # -----------------------------
                    # Final Result
                    # -----------------------------

                    st.markdown("---")

                    if result["ats_score"] >= 80:

                        st.success(
                            "Excellent ATS compatibility! "
                            "Your resume matches the job description well."
                        )

                    elif result["ats_score"] >= 60:

                        st.warning(
                            "Good resume, but some improvements "
                            "can increase your ATS score."
                        )

                    else:

                        st.error(
                            "Your resume needs improvement "
                            "to achieve better ATS compatibility."
                        )


            except Exception as e:

                st.error(
                    f"Error while analyzing resume: {e}"
                )


# -----------------------------
# Footer
# -----------------------------

st.markdown("---")

st.caption(
    "AI Resume Analyzer & ATS Optimizer | Built with Python & Streamlit"
)