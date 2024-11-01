from datetime import time, datetime
from django.shortcuts import render
import google.generativeai as genai
import os
import tempfile
from dotenv import load_dotenv
import markdown
from docx2pdf import convert
from pathlib import Path
import uuid

# Get the current year and month for display purposes
current_year = datetime.now().year
current_month = datetime.now().month
current_month_name = datetime.now().strftime("%B")

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

def get_unique_temp_path(suffix):
    """Generate a unique temporary file path"""
    unique_filename = f"resume_temp_{uuid.uuid4().hex}{suffix}"
    return os.path.join(tempfile.gettempdir(), unique_filename)

def convert_docx_to_pdf(docx_path):
    """Convert DOCX file to PDF format"""
    pdf_path = get_unique_temp_path('.pdf')
    convert(docx_path, pdf_path)
    return pdf_path

def safe_remove_file(file_path):
    """Safely remove a file if it exists"""
    try:
        if file_path and os.path.exists(file_path):
            os.close(os.open(file_path, os.O_RDONLY))  # Close any open handles
            os.remove(file_path)
    except Exception as e:
        print(f"Error removing file {file_path}: {str(e)}")

def parse_resume(file_path, mime_type):
    """Parse resume file and extract key information using Google Generative AI"""
    temp_pdf_path = None
    
    try:
        # If the file is DOCX, convert it to PDF first
        if mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            temp_pdf_path = convert_docx_to_pdf(file_path)
            upload_path = temp_pdf_path
            upload_mime_type = 'application/pdf'
        else:
            upload_path = file_path
            upload_mime_type = mime_type

        # Upload the file to Google Generative AI service
        file = genai.upload_file(upload_path, mime_type=upload_mime_type)
        name = file.name

        # Poll for file processing status
        while True:
            file = genai.get_file(name)
            if file.state.name == "ACTIVE":
                break
            elif file.state.name != "PROCESSING":
                raise Exception(f"File {file.name} failed to process")
            time.sleep(10)

        # Define extraction query
        extraction_query = (
            "Extract the following fields from the resume and display each content in book format in full detail with proper text styles:"
            "First Name: , Last Name : , Email Address, Phone Number, Education Details, "
            "Work Experience Details, Skills, Current Position, "
            f"Years of Experience(Iterate through each experiance and sum up experiance based on month,year specified (show calculation summary (startmonth_year-endmonth_year )) , IMP NOTE :if mentioned..'present' or...in semantic meaning currenly working means..todays month is {current_month_name},{current_year} use for calculation minus 1)."
            f"Calculate years of Experiance of current job accurately considering as endMonth,year as({current_month_name},{current_year}) double check the answer -->final_result should be in [years and months]. "
        )

        # Initialize chat session
        chat_session = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 5000,
                "response_mime_type": "text/plain",
            },
        ).start_chat(history=[{"role": "user", "parts": [file]}])

        return chat_session.send_message(extraction_query).text

    finally:
        # Clean up temporary PDF file if it was created
        safe_remove_file(temp_pdf_path)

def upload_resume(request):
    """Handle resume upload and display parsed results"""
    temp_file_path = None
    
    if request.method == "POST" and request.FILES['resume']:
        uploaded_file = request.FILES['resume']
        file_extension = f".{uploaded_file.name.split('.')[-1]}"
        
        try:
            # Create temporary file with unique name
            temp_file_path = get_unique_temp_path(file_extension)
            
            # Write uploaded file content
            with open(temp_file_path, 'wb') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)
            
            # Parse resume and get result
            result = parse_resume(temp_file_path, mime_type=uploaded_file.content_type)
            result = markdown.markdown(result)
            
            return render(request, 'parser_app/index.html', {
                'result': result, 
                'current_year': current_year
            })
            
        except Exception as e:
            return render(request, 'parser_app/index.html', {
                'error': f"Error processing file: {str(e)}",
                'current_year': current_year
            })
            
        finally:
            # Clean up temporary file
            safe_remove_file(temp_file_path)
    
    return render(request, 'parser_app/index.html', {'current_year': current_year})