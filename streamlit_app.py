import streamlit as st
import base64
import nltk
import os 
from sentence_transformers import SentenceTransformer

from pdf_loader import load_btyes_io, load_documents
from core import pipeline

sample_files = [
    "Mehul Soni_Resume.pdf",
    "Chia Wei Jie_Resume.pdf",
    "Sam Zhuo Li_Resume.pdf",
]        

sample_job_descriptions = {
    "Business Management": """Job Title: Accountant
    Responsibilities:
        Prepare financial statements and reports for management and external stakeholders.
        Manage general ledger entries, accounts payable, and accounts receivable.
        Conduct financial analysis and assist in budgeting and forecasting processes.
        Ensure compliance with accounting principles and regulations.
        Collaborate with auditors during financial audits and provide necessary documentation.
    Required Skills:
        Proficiency in financial reporting and accounting principles.
        Experience with budgeting, auditing, and taxation processes.
        Familiarity with accounting software and tools (e.g., Excel, QuickBooks).
        Strong attention to detail and accuracy in financial data analysis.
        Effective communication and interpersonal skills.""",
    "Mobile Engineer": """Job Title: Mobile Engineer
    Responsibilities:
        Develop and maintain mobile applications using Flutter framework.
        Collaborate with the backend team to integrate APIs and implement required functionalities.
        Work on bug fixing and improving application performance.
        Conduct code reviews and ensure code quality.
        Stay updated with the latest trends and technologies in mobile app development.
    Required Skills:
        Proficiency in Flutter, Dart, and mobile app development.
        Experience with Spring Boot and backend development is a plus.
        Knowledge of software development principles and best practices.
        Familiarity with frontend and backend technologies such as JavaScript, Java, and MongoDB.
        Strong problem-solving and analytical thinking skills.""",
    "Data Scientist": """    Job Title: Data Scientist
    Responsibilities:
        Analyze complex data sets to derive meaningful insights and patterns.
        Build and deploy machine learning models for predictive analysis and data mining.
        Collaborate with cross-functional teams to identify business requirements and formulate data-driven solutions.
        Cleanse and preprocess data for analysis, ensuring data quality and integrity.
        Communicate findings and present actionable insights to stakeholders.
    Required Skills:
        Proficiency in Python, SQL and data manipulation libraries (e.g., Pandas, NumPy).
        Experience in machine learning techniques and frameworks (e.g., Scikit-learn, TensorFlow, PyTorch).
        Strong statistical analysis skills and familiarity with statistical modeling techniques.
        Knowledge of data visualization tools (e.g., Matplotlib, Seaborn) to present results effectively.
        Excellent problem-solving and critical-thinking abilities."""
}

# Load the models and ntlk packages
download_path = os.path.join(os.getcwd(), 'nltk_packages')
nltk.data.path.append(download_path)
nltk.download('wordnet', download_dir=download_path)
nltk.download('stopwords', download_dir=download_path)
nltk.download('punkt', download_dir=download_path)
sbert_model = SentenceTransformer('bert-base-nli-mean-tokens', cache_folder=os.path.join(os.getcwd(), 'models'))

def inference(query, strings, embedding_type):
    results, _ = pipeline(query, strings , embedding_type=embedding_type)
    return results

def resume_ranker():
    # Add a header to the main page
    st.title("📜Resume Ranker")

    selected_job = st.sidebar.selectbox("Select a job description", list(sample_job_descriptions.keys()))
    query = st.text_area("Job Description - enter skills, job description, or keywords here", height=200, placeholder='keywords', value=sample_job_descriptions[selected_job])
    uploaded_files = st.file_uploader("Upload Resume - up to 10", accept_multiple_files=True, type=["txt", "pdf"])

    # Sample Resumes
    selected_sample_files = st.multiselect("Or select our sample resumes", sample_files)

    embedding_type = st.selectbox("Embedding Type", ["sbert", "minilm", "tfidf"])

    if st.button("Rank 'Em Resumes!"):
        if not query:
            st.warning("Please enter a job description.")
        elif (not uploaded_files) and (not selected_sample_files):
            st.warning("Please upload one or more resumes.")
        else:
            with st.spinner("Processing..."):
                if selected_sample_files and uploaded_files:
                    uploaded_files = load_btyes_io(uploaded_files) + load_documents([f"documents/{file}" for file in selected_sample_files])
                    results = inference(query, uploaded_files, embedding_type)
                elif selected_sample_files:
                    uploaded_files = load_documents([f"documents/{file}" for file in selected_sample_files])
                    results = inference(query, uploaded_files, embedding_type)
                else:
                    uploaded_files = load_btyes_io(uploaded_files)
                    results = inference(query, uploaded_files , embedding_type)
            st.subheader("Results")
            for result in results:
                similarity = result["similarity"]
                if similarity > 1:
                    similarity = 1.0
                elif similarity < 0:
                    similarity = 0.0
                name = result["name"]
                rank = result["rank"]
                # make similiarty round to 2 decimal place
                if similarity >= 1:
                    similarity = round(similarity, 2)
                if rank == 0:
                    st.text(f"👑Rank {rank + 1} - {name} ")
                else:
                    st.text(f"Rank {rank + 1} - {name} ")
                st.progress(similarity, text=f"{similarity:.2%}")

def resume_viewer():
    st.title("👨🏼‍🎓Resume Viewer")
    selected_file = st.selectbox('Select a resume', sample_files)

    def show_pdf(selected_file):
        with open(f'documents/{selected_file}',"rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">' 
        st.markdown(pdf_display, unsafe_allow_html=True)
    
    show_pdf(selected_file)

page_names_to_funcs = {
    "Resume Ranker": resume_ranker,
    "Resume Viewer": resume_viewer
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()