from flask import Flask, request, render_template
from review_engine import analyze_contract
from pdf_utils import extract_text_from_pdf
import docx
import json
import csv

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max upload

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'json', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(file, ext):
    if ext == 'pdf':
        return extract_text_from_pdf(file)
    elif ext == 'docx':
        document = docx.Document(file)
        return '\n'.join([para.text for para in document.paragraphs])
    elif ext == 'txt':
        return file.read().decode('utf-8')
    elif ext == 'json':
        data = json.load(file)
        return json.dumps(data, indent=2)
    elif ext == 'csv':
        decoded = file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded)
        return '\n'.join([', '.join(row) for row in reader])
    else:
        return ''

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    result = None
    error = None
    text = ''

    if 'contract_file' in request.files:
        file = request.files['contract_file']
        filename = file.filename.lower()

        if file and allowed_file(filename):
            ext = filename.rsplit('.', 1)[1]
            text = extract_text(file, ext)
            if not text.strip():
                error = "The uploaded file seems to be empty or unreadable."
            else:
                result = analyze_contract(text)
        else:
            error = "Unsupported file type. Please upload a valid PDF, DOCX, TXT, JSON, or CSV file."

    elif 'contract' in request.form:
        text = request.form['contract']
        if not text.strip():
            error = "You submitted an empty contract."
        else:
            result = analyze_contract(text)

    return render_template('index.html', result=result, error=error, preview=text[:500], filename=file.filename if 'file' in locals() else None)


if __name__ == '__main__':
    app.run(debug=True)
