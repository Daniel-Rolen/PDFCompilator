from flask import Flask, render_template, jsonify, request, send_from_directory, send_file
import os
import json
from pdf_compiler import compile_pdfs, get_pdf_info, parse_page_range
from name_generator import generate_space_name
from PyPDF2 import PdfReader
from io import BytesIO
import fitz  # PyMuPDF

app = Flask(__name__)

# Initialize an empty list to store PDF file names
pdf_files = []

# Add a version number for cache busting
STATIC_VERSION = "3"

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

@app.route('/reorder_pdfs', methods=['POST'])
def reorder_pdfs():
    old_index = request.json.get('oldIndex')
    new_index = request.json.get('newIndex')
    
    if old_index is not None and new_index is not None:
        pdf_files.insert(new_index, pdf_files.pop(old_index))
        return jsonify(success=True, message="PDF order updated successfully")
    return jsonify(success=False, message="Invalid indices provided")

@app.route('/preview_pdf/<pdf_name>')
def preview_pdf(pdf_name):
    if pdf_name in pdf_files:
        try:
            # Open the PDF file
            pdf_document = fitz.open(pdf_name)
            
            # Get the first page
            page = pdf_document[0]
            
            # Render the page as a PNG image
            pix = page.get_pixmap()
            img_bytes = pix.tobytes("png")
            
            # Close the PDF document
            pdf_document.close()
            
            # Send the image as a response
            return send_file(
                BytesIO(img_bytes),
                mimetype='image/png'
            )
        except Exception as e:
            return jsonify(success=False, message=f"Error generating preview: {str(e)}")
    return jsonify(success=False, message="PDF not found")

@app.route('/pdf_info/<pdf_name>')
def pdf_info(pdf_name):
    if pdf_name in pdf_files:
        try:
            info = get_pdf_info(pdf_name)
            return jsonify(info)
        except Exception as e:
            return jsonify(success=False, message=f"Error fetching PDF info: {str(e)}")
    return jsonify(success=False, message="PDF not found")

if __name__ == '__main__':
    if not os.path.exists("output"):
        os.makedirs("output")
    app.run(host='0.0.0.0', port=8080, debug=True)
