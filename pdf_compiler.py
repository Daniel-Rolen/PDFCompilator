import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_cover_page(output_path, title):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height / 2, title)
    c.save()

def compile_pdfs(input_files, output_file, use_cover_pages=False, cover_pages=None):
    writer = PdfWriter()
    
    if use_cover_pages:
        cover_page_path = "cover_page.pdf"
        create_cover_page(cover_page_path, "Compiled PDF")
        writer.append(cover_page_path)

    for input_file in input_files:
        reader = PdfReader(input_file)
        if cover_pages and input_file == input_files[0]:
            for page_num in parse_page_range(cover_pages, len(reader.pages)):
                writer.add_page(reader.pages[page_num - 1])
        else:
            writer.append(input_file)

    with open(output_file, "wb") as f:
        writer.write(f)

    if use_cover_pages:
        os.remove(cover_page_path)

def parse_page_range(page_range_str, max_pages):
    pages = set()
    ranges = page_range_str.split(',')
    for r in ranges:
        if '-' in r:
            start, end = map(int, r.split('-'))
            pages.update(range(start, min(end + 1, max_pages + 1)))
        else:
            page = int(r)
            if page <= max_pages:
                pages.add(page)
    return sorted(pages)

def get_pdf_info(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf = PdfReader(file)
            info = pdf.metadata
            num_pages = len(pdf.pages)
            file_size = os.path.getsize(file_path)
            
            return {
                'filename': os.path.basename(file_path),
                'num_pages': num_pages,
                'file_size': f"{file_size / 1024:.2f} KB",
                'created_date': info.creation_date.strftime('%Y-%m-%d %H:%M:%S') if info.creation_date else "N/A",
                'modified_date': info.modification_date.strftime('%Y-%m-%d %H:%M:%S') if info.modification_date else "N/A"
            }
    except Exception as e:
        print(f"Error getting PDF info: {str(e)}")
        return None

# Explicitly export the functions
__all__ = ['compile_pdfs', 'get_pdf_info', 'parse_page_range']
