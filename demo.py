from pdf_loader import load_documents
from core import pipeline

if __name__ == '__main__':
    pipeline("""Job Title: Mobile Engineer
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
                   load_documents(source_dir = 'documents'))
