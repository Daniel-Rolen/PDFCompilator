from flask import Flask, render_template, jsonify, request, send_from_directory
import os
import json

app = Flask(__name__)

# Initialize an empty list to store PDF file names
pdf_files = []

@app.route('/')
def index():
    return render_template('index.html')

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
    # This is a placeholder for the actual PDF compilation logic
    return jsonify(success=True, message="PDFs compiled successfully", files=pdf_files)

@app.route('/get_pdfs', methods=['GET'])
def get_pdfs():
    return jsonify(pdf_files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
