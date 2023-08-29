from flask import Flask, request, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
import fitz  # Para PDFs (PyMuPDF)

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verifica se o arquivo foi enviado e tem a extensão permitida
        if 'pdf' not in request.files:
            return "Nenhum arquivo enviado"
        
        pdf_file = request.files['pdf']
        if pdf_file.filename == '':
            return "Nenhum arquivo selecionado"
        
        if pdf_file and allowed_file(pdf_file.filename):
            filename = secure_filename(pdf_file.filename)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            pdf_file.save(pdf_path)

            # Atualiza a lista de arquivos enviados
            pdf_files = os.listdir(app.config['UPLOAD_FOLDER'])
    
            return render_template('index.html', pdf_files=pdf_files)
    
    # Lista os arquivos PDF na pasta de uploads
    pdf_files = os.listdir(app.config['UPLOAD_FOLDER'])
    
    return render_template('index.html', pdf_files=pdf_files)

@app.route('/pdf/<filename>')
def serve_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

app.run(host='localhost', port=5000)
