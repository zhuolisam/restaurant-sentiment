import streamlit as st
from pdf_loader import load_btyes_io, load_documents
import base64
from core import pipeline

sample_files = [
    "Chia Wei Jie_Resume.pdf",
    "Sam Zhuo Li_Resume.pdf",
    "Fong Shi Hui_Resume.pdf",
]        

sample_job_descriptions = {
    "Business Management": """Microsoft Office Excel Word PowerPoint Access Video Editing Adobe Photoshop Software Excel Analytical Thinking Attention to Detail Communication Skills""",
    "Mobile Engineer": """Flutter Springboot Software Development Python Java Provider Frontend Backend Fullstack Developer MongoDB MySQL""",
    "Data Scientist": """Python SQL Machine Learning Deep Learning PyTorch Tensorflow Keras Scikit-learn Numpy Pandas"""
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
        # pdf_url = 'https://drive.google.com/file/d/13fbfMOl3Pjgo5kaNeDZ7nP1cZQvIA6x3/view'
        # pdf_display = F'<iframe src="{pdf_url}" width="700" height="700" type="application/pdf"></iframe>'    # st.markdown(f'<a href="./documents/{selected_file}" >{selected_file}</a>', unsafe_allow_html=True)
        st.markdown(pdf_display, unsafe_allow_html=True)
    
    show_pdf(selected_file)

page_names_to_funcs = {
    "Resume Ranker": resume_ranker,
    "Resume Viewer": resume_viewer
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()