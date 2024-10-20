import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_cover_page(output_path, title):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height / 2, title)
    c.save()

def compile_pdfs(input_files, output_file, use_cover_pages=False, cover_pages=None):
    merger = PdfMerger()
    
    if use_cover_pages:
        cover_page_path = "cover_page.pdf"
        create_cover_page(cover_page_path, "Compiled PDF")
        merger.append(cover_page_path)

    for input_file in input_files:
        if cover_pages and input_file == input_files[0]:
            pdf = PdfReader(input_file)
            writer = PdfWriter()
            for page_num in parse_page_range(cover_pages, len(pdf.pages)):
                writer.add_page(pdf.pages[page_num - 1])
            temp_output = f"temp_{os.path.basename(input_file)}"
            with open(temp_output, "wb") as f:
                writer.write(f)
            merger.append(temp_output)
            os.remove(temp_output)
        else:
            merger.append(input_file)

    merger.write(output_file)
    merger.close()

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
