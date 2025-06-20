import pdfkit
from flask import Flask, request, render_template, flash, redirect, url_for, send_file
from PyPDF2 import PdfReader
from subjective import SubjectiveTest
import re
import os
from urllib.parse import quote
import base64

app = Flask(__name__)
app.secret_key = 'aica2'

# Path to wkhtmltopdf executable for PDF generation
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

@app.route('/')
def index():
    """Render the home page."""
    return render_template('front.html')

@app.route('/predict')
def index1():
    """Render the skill/question prediction page."""
    return render_template('predict.html')

@app.route('/scorer')
def index2():
    """Render the resume scoring page."""
    return render_template('scorer.html')

@app.route('/test_generate', methods=["POST"])
def test_generate():
    """
    Handle PDF upload, extract skills, and generate subjective questions.
    """
    if 'pdf_file' not in request.files:
        flash("No file part")
        return redirect(url_for('index1'))
    
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        flash("No selected file")
        return redirect(url_for('index1'))
    
    if pdf_file:
        # Read PDF and extract text
        pdf = PdfReader(pdf_file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    
    # Extract skills from resume text
    skills = extract_skills(text)
    valid_keywords = ["Python", "programming", "machine learning", "data analysis", "NLP", "OOPs", "Java"]
    no_of_questions = 150  # Number of questions to generate

    try:
        # Generate subjective questions based on skills
        subjective_generator = SubjectiveTest(skills, no_of_questions, valid_keywords)
        question_list = subjective_generator.generate_questions()
        return render_template('predict.html', cresults=question_list)
    except Exception as e:
        flash(f'Error Occurred: {str(e)}')
        return redirect(url_for('index1'))

@app.route("/generate")
def gen():
    """Render the resume generation form."""
    return render_template('generate.html')

@app.route("/generatepdf", methods=['POST'])
def generatepdf():
    """
    Generate a PDF resume from form data and return it for download.
    """
    if request.method == "POST":
        form_data = request.form
        # Extract form fields
        name = form_data['Name']
        email = form_data['Email']
        linkedin = form_data['LinkedIn']
        experience = form_data['Experience']
        skills = form_data['Skills'].splitlines()
        internship = form_data['Internship'].splitlines()
        achievements = form_data['Achievements'].splitlines()
        projects = form_data['projects'].splitlines()
        description = form_data['Description']
        selected_template = form_data['template']

        # Handle photo upload
        photo_data = None
        photo_file = request.files.get('photo')
        if photo_file:
            photo_data = base64.b64encode(photo_file.read()).decode('utf-8')

        # Collect education entries
        education_entries = []
        for key in form_data:
            if key.startswith("education"):
                parts = key.split('[')
                index = int(parts[1].split(']')[0])  
                field_name = parts[2].split(']')[0]
                if len(education_entries) <= index:
                    education_entries.append({})
                education_entries[index][field_name] = form_data[key]

        # Render HTML and generate PDF
        html_content = render_template(
            selected_template,
            name=name,
            photo_data=photo_data,
            email=email,
            linkedin=linkedin,
            experience=experience,
            education_entries=education_entries,
            projects=projects,
            skills=skills,
            internship=internship,
            achievements=achievements,
            description=description
        )

        pdf_path = os.path.join('static', 'uploads', 'resume.pdf')
        try:
            pdfkit.from_string(html_content, pdf_path, configuration=config)
            if os.path.exists(pdf_path):
                return send_file(pdf_path, as_attachment=True)
            else:
                flash("PDF generation failed.")
                return redirect(url_for('gen'))
        except Exception as e:
            flash(f'Error generating PDF: {str(e)}')
            return redirect(url_for('gen'))
    return render_template('cantdownload.html')

@app.route("/score_resume", methods=["GET", "POST"])
def score_resume():
    """
    Handle PDF upload and score the resume based on extracted information.
    """
    if request.method == "POST":
        if 'pdf_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        pdf_file = request.files['pdf_file']
        if pdf_file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if pdf_file:
            pdf = PdfReader(pdf_file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            resume_data = {
                'Name': extract_name(text),
                'Email': extract_email(text),
                'LinkedIn': extract_linkedin(text),
                'Experience': extract_experience(text),
                'Education': extract_education_details(text),
                'Skills': extract_skills(text),
                'Internship': extract_internship(text),
                'Achievements': extract_achievements(text),
                'Projects': extract_projects(text)
            }
            resume_score = calculate_score(resume_data)
            return render_template('score_result.html', score=resume_score)
    
    return render_template('score_upload.html')

def extract_name(text):
    """Extracts a probable name from the resume text."""
    match = re.search(r"([A-Z][a-z]+(?: [A-Z][a-z]+)+)", text)
    return match.group(1).strip() if match else "Name not found"

def extract_email(text):
    """Extracts the email address from the resume text."""
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0).strip() if match else "Email not found"

def extract_linkedin(text):
    """Extracts LinkedIn URL from the resume text."""
    match = re.search(r"(https?://www\.linkedin\.com/in/[A-Za-z0-9-]+|LinkedIn)", text, re.IGNORECASE)
    return match.group(0).strip() if match else "LinkedIn not found"

def extract_github(text):
    """Extracts GitHub URL from the resume text."""
    match = re.search(r"(https?://github\.com/[A-Za-z0-9-]+|GitHub)", text, re.IGNORECASE)
    return match.group(0).strip() if match else "GitHub not found"

def extract_experience(text):
    """Estimates years of experience by identifying date ranges in work history."""
    experience_pattern = r"(?:April|May|June|July|August|September|October|November|December) \d{4}"
    matches = re.findall(experience_pattern, text)
    return len(matches) if matches else 0

def extract_education_details(text):
    """Extracts educational details including highest education level, CGPA, and university name."""
    education_matches = re.findall(r"(BTech|Bachelor|Diploma|Master|PhD) in [A-Za-z ]+", text, re.IGNORECASE)
    cgpa_match = re.search(r"GPA\s*[-:]?\s*(\d+\.\d+)", text)
    university_match = re.search(r"[A-Za-z ]+(?:Institute|University|College)", text)
    return {
        "highest_education": education_matches if education_matches else ["Education not found"],
        "cgpa": float(cgpa_match.group(1)) if cgpa_match else 0.0,
        "university": university_match.group(0).strip() if university_match else "University not found"
    }

def extract_skills(text):
    """Extracts and formats programming languages, frameworks/libraries, databases, or other skills."""
    programming_match = re.search(r"Programming Languages ?:?\s*([A-Za-z+, ]+)", text, re.IGNORECASE)
    frameworks_match = re.search(r"Frameworks/Libraries ?:?\s*([A-Za-z., ]+)", text, re.IGNORECASE)
    databases_match = re.search(r"Databases ?:?\s*([A-Za-z, ]+)", text, re.IGNORECASE)
    skills_match = re.search(r"(Skills|Expertise)\s*[-•*]?\s*([A-ZaZ0-9+.,\s]+?)(?=\n*Experience|Achievements|$)", text, re.IGNORECASE)
    
    skills = []
    
    if programming_match:
        skills.extend(programming_match.group(1).strip().lower().split(","))
    if frameworks_match:
        frameworks = frameworks_match.group(1).strip().lower()
        skills.extend(frameworks.split(","))
    if databases_match:
        skills.extend(databases_match.group(1).strip().lower().split(","))

    if skills_match:
        raw_skills = skills_match.group(2).replace("\n", " ").lower().strip()  
        skills.extend([skill.strip() for skill in raw_skills.split(",")])
    
    return [s.strip() for s in skills if s.strip()]

def extract_internship(text):
    """Identifies internships by searching for keywords."""
    match = re.search(r"(Trainee|Intern|Internship)", text, re.IGNORECASE)
    return match.group(0).strip() if match else "Internship not found"

def extract_achievements(text):
    """Extracts achievements from the resume text, assuming a list format."""
    match = re.search(r"Achievements(?:\n|:| -)\s*(?:•\s*)?([A-Za-z, 0-9]+(?:\n• [A-Za-z, 0-9]+)*)", text, re.IGNORECASE)
    return match.group(1).strip().split('\n• ') if match else ["Achievements not found"]

def extract_projects(text):
    """Extracts project information from the resume text, assuming a list format."""
    match = re.search(r"Projects(?:\n|:| -)\s*(?:•\s*)?([A-Za-z, 0-9]+(?:\n• [A-ZaZ0-9]+)*)", text, re.IGNORECASE)
    return match.group(1).strip().split('\n• ') if match else ["Projects not found"]

def calculate_score(resume_data):
    max_points = {
        'Name': 5,
        'Email': 5,
        'LinkedIn': 10,
        'GitHub': 10,
        'Experience': 20,
        'Education': 15,
        'Skills': 15,
        'Internship': 5,
        'Achievements': 5,
        'Projects': 10
    }
    
    score = 0

    if resume_data['Name'] != "Name not found":
        score += max_points['Name']

    if resume_data['Email'] != "Email not found":
        score += max_points['Email']

    if resume_data['LinkedIn'] != "LinkedIn not found":
        score += max_points['LinkedIn']
    
    if 'GitHub' in resume_data and resume_data['GitHub'] != "GitHub not found":
        score += max_points['GitHub']

    experience_years = resume_data['Experience']
    score += min(max_points['Experience'], experience_years * 5)

    if resume_data['Education'] and len(resume_data['Education']) >= 1:
        score += max_points['Education']

    skills_count = len(set(resume_data['Skills']))
    score += min(max_points['Skills'], skills_count * 2)  

    if resume_data['Internship'] != "Internship not found":
        score += max_points['Internship']

    if resume_data['Achievements'] != "Achievements not found":
        achievements_count = len(resume_data['Achievements'])
        score += min(max_points['Achievements'], achievements_count * 2)  

    projects_count = len(resume_data['Projects'])
    score += min(max_points['Projects'], projects_count * 2)  

    final_score = min(100, score)
    return round(final_score, 2)

if __name__ == "__main__":
    app.run(debug=True)
