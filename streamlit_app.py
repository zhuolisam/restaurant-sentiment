import streamlit as st
from pdf_loader import load_btyes_io, load_documents
import base64
from core import pipeline

sample_files = [
    "business.pdf",
    "data_science.pdf",
]        

sample_job_descriptions = {
    "Software Engineer": """We are looking for a software engineer with experience in Python and web development. The ideal candidate should have a strong background in building scalable and robust applications. Knowledge of frameworks such as Flask and Django is a plus. Experience with front-end technologies like HTML, CSS, and JavaScript is desirable. The candidate should also have a good understanding of databases and SQL. Strong problem-solving and communication skills are required for this role.
    """,
    "Data Scientist": """We are seeking a data scientist with expertise in machine learning and statistical analysis. The candidate should have a solid understanding of data manipulation, feature engineering, and model development. Proficiency in Python and popular data science libraries such as NumPy, Pandas, and Scikit-learn is required. Experience with deep learning frameworks like TensorFlow or PyTorch is a plus. Strong analytical and problem-solving skills are essential for this position.
    """
}

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

    embedding_type = st.selectbox("Embedding Type", ["bert", "minilm", "tfidf"])
    if st.button("Rank 'Em Resumes!"):
        if not query:
            st.warning("Please enter a job description.")
        elif (not uploaded_files) and (not selected_sample_files):
            st.warning("Please upload one or more resumes.")
        else:
            with st.spinner("Processing..."):
                if selected_sample_files and uploaded_files:
                    uploaded_files = load_btyes_io(uploaded_files) + load_documents([f"./documents/{file}" for file in selected_sample_files])
                    results = inference(query, uploaded_files, embedding_type)
                elif selected_sample_files:
                    uploaded_files = load_documents([f"./documents/{file}" for file in selected_sample_files])
                    results = inference(query, uploaded_files, embedding_type)
                else:
                    uploaded_files = load_btyes_io(uploaded_files)
                    results = inference(query, uploaded_files , embedding_type)
            st.subheader("Results")
            for result in results:
                similarity = result["similarity"]
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
    with open(f'documents/{selected_file}',"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

page_names_to_funcs = {
    "Resume Ranker": resume_ranker,
    "Resume Viewer": resume_viewer
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()