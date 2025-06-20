# CVMap.AI

CVMap.AI is a Flask-based web application for:
- Extracting skills from uploaded PDF resumes
- Generating subjective questions based on those skills
- Scoring resumes on various parameters
- Generating resume PDFs from user input

---

## Features

- **Skill Extraction:** Upload a PDF resume and extract key skills automatically.
- **Subjective Question Generation:** Generate a list of subjective questions tailored to the extracted skills.
- **Resume Scoring:** Score resumes based on the presence of important sections like Name, Email, LinkedIn, Experience, Education, Skills, Internships, Achievements, and Projects.
- **Resume PDF Generation:** Fill out a form to generate a professional resume PDF using customizable templates.

---

## Getting Started

### 1. Clone the Repository

```sh
git clone <repository-url>
cd CVMap.AI
```

### 2. Install Python Dependencies

Make sure you have Python 3.7+ installed. Then run:
```sh
pip install flask PyPDF2 pdfkit numpy nltk
```

### 3. Install wkhtmltopdf

- Download and install [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) for your operating system.
- Update the `path_to_wkhtmltopdf` variable in `app.py` if your installation path is different.

### 4. Download NLTK Data

Run the following Python code once to download all necessary NLTK data:
```python
import nltk
nltk.download('all')
```

### 5. Run the Application

```sh
python app.py
```

### 6. Access the App

Open your browser and go to:  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Project Structure

```
CVMap.AI/
│
├── app.py                # Main Flask application (with comments)
├── subjective.py         # Subjective question generator logic
├── templates/            # HTML templates for the web interface
├── static/               # Static files (CSS, JS, uploads, etc.)
└── README.md             # Project documentation
```

---

## Usage

- **Skill Extraction & Question Generation:**  
  Go to the "Predict" page, upload your resume PDF, and view the generated questions.

- **Resume Scoring:**  
  Go to the "Scorer" page, upload your resume PDF, and view your resume score.

- **Resume PDF Generation:**  
  Go to the "Generate" page, fill out the form, and download your generated resume PDF.

---

## Notes

- Ensure the `static/uploads` directory exists and is writable for PDF generation and downloads.
- The application is designed for local use and educational/demo purposes.

---

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---