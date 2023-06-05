import os
import PyPDF2

def load_single_document(file_path: str):
    # Loads a single document from file path
    if file_path[-4:] == '.txt':
        with open(file_path, 'r') as f:
            return f.read()

    elif file_path[-4:] == '.pdf':
        pdfFileObj = open(file_path, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        text = ''
        for page in pdfReader.pages:
            text += page.extract_text()
        return text

    elif file_path[-4:] == '.csv':
        with open(file_path, 'r') as f:
            return f.read()

    else:
        raise Exception('Invalid file type')


def load_documents(file_paths: list[str] = None, source_dir: str = None):
    # Loads all documents from source documents directory
    if file_paths:
        all_files = file_paths
    elif source_dir:
        all_files = [os.path.abspath(os.path.join(source_dir, file)) for file in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, file))]
    else:
        raise Exception('No file paths or source directory provided')

    return [
            {
                'name': os.path.basename(file_path),
                'content': load_single_document(f"{file_path}")
            } for idx, file_path in enumerate(all_files) if file_path[-4:] in ['.txt', '.pdf', '.csv']
        ]
