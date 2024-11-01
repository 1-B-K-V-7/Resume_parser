# Resume_parser

Video Demonstration link : https://drive.google.com/file/d/1eONcZkaNe2-Mzmkin9nTBwiWM7vVR9Uu/view?usp=sharing  

This project is a web application that allows users to upload their resumes (in DOCX or PDF format) and extracts key information using LLM. The extracted data is displayed in a well-formatted manner for easy review.

## Table of Contents

- Features
- Technologies Used
- Setup
- Running the Application
- Environment Variables
- Concept and Working


## Features

- Upload resumes in DOCX or PDF formats.
- Extracts various fields from the resume, including personal details, education, work experience, and skills.
- Presents the extracted information in a user-friendly format.

## Technologies Used

- Django
- LLM-Google Generative AI API (gemini-1.5-flash)

## Setup

1. **Clone the repository:**
   
   git clone https://github.com/1-B-K-V-7/Resume_parser.git
   
   cd Resume_parser

2 Create a virtual environment: python -m venv env

3 Activate the virtual environment:

On Windows: .\env\Scripts\activate

On macOS/Linux: source env/bin/activate

4 Install the required packages:
pip install -r requirements.txt

5 Set up the environment variables:
Create a .env file in the root directory of the project and add the following line: API_KEY=your_google_api_key_here

6 Running the Application
Run the Django development server: python manage.py runserver
Access the application: Open your web browser and navigate to http://127.0.0.1:8000.

Environment Variables
API_KEY: This variable holds your Google Generative AI API key. It is required for interacting with the AI service to parse resumes.



## Concept and Working

File Upload: Users can upload resumes in either DOCX or PDF format through the web interface.
File Conversion: If the uploaded file is a DOCX, the application converts it to PDF using docx2pdf.

File Processing:
The application uploads the resume file to Google Generative AI for processing.
A polling mechanism checks the status of the file processing until it is complete.

Data Extraction: The application constructs a query to extract specific fields from the resume, including:
First Name
Last Name
Email Address
Phone Number
Education Details
Work Experience Details
Skills
Current Position
Years of Experience (calculated accurately based on the current date)
Result Presentation: The extracted data is formatted using Markdown and displayed on the web interface.


## Assumptions and Limitations
The application is designed for DOCX and PDF formats, and deviations from these may lead to errors in processing. It relies on structured resumes, meaning unconventional layouts may impact data extraction accuracy.

## Future Improvements
Future iterations aim to enhance parsing accuracy with unstructured resumes  and support additional file formats for user convenience. Improvements will also focus on developing a more interactive UI for editing parsed data and refining error handling for clearer user guidance.

                                                           ****************
