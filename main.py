from flask import Flask, render_template, jsonify, request, send_from_directory
import os
import json
from pdf_compiler import compile_pdfs
from name_generator import generate_space_name

app = Flask(__name__)

# Initialize an empty list to store PDF file names
pdf_files = []

# Add a version number for cache busting
STATIC_VERSION = "1"

@app.route('/')
def index():
    return render_template('index.html', static_version=STATIC_VERSION)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/add_pdf', methods=['POST'])
def add_pdf():
    pdf_name = request.json.get('name')
    if pdf_name and pdf_name not in pdf_files:
        pdf_files.append(pdf_name)
        return jsonify(success=True, message=f"Added {pdf_name}")
    return jsonify(success=False, message="Invalid PDF name or already exists")

@app.route('/remove_pdf', methods=['POST'])
def remove_pdf():
    pdf_name = request.json.get('name')
    if pdf_name in pdf_files:
        pdf_files.remove(pdf_name)
        return jsonify(success=True, message=f"Removed {pdf_name}")
    return jsonify(success=False, message="PDF not found")

@app.route('/compile_pdf', methods=['POST'])
def compile_pdf():
    use_cover_pages = request.json.get('useCoverPages', False)
    cover_pages = request.json.get('coverPages', '')
    output_filename = generate_space_name() + ".pdf"
    output_path = os.path.join("output", output_filename)
    
    try:
        compile_pdfs(pdf_files, output_path, use_cover_pages, cover_pages)
        return jsonify(success=True, message=f"PDFs compiled successfully as {output_filename}", files=pdf_files, useCoverPages=use_cover_pages, coverPages=cover_pages)
    except Exception as e:
        return jsonify(success=False, message=f"Error compiling PDFs: {str(e)}")

@app.route('/get_pdfs', methods=['GET'])
def get_pdfs():
    return jsonify(pdf_files)

if __name__ == '__main__':
    if not os.path.exists("output"):
        os.makedirs("output")
    app.run(host='0.0.0.0', port=8080, debug=True)
